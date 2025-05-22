import argparse
import json
import logging
from pathlib import Path

from trestle.common.err import TrestleError, TrestleNotFoundError
from trestle.core.catalog.catalog_api import CatalogAPI
from trestle.core.catalog.catalog_interface import CatalogInterface
from trestle.core.commands.common.return_codes import CmdReturnCodes
from trestle.core.control_context import ContextPurpose, ControlContext
from trestle.core.control_interface import ControlInterface
from trestle.oscal.catalog import Catalog
from trestle.oscal.common import Parameter

logger = logging.getLogger("compliance-pipeline")
log_format = "[%(asctime)s %(levelname)s %(name)s] %(message)s"
logging.basicConfig(format=log_format)


class TrestleCLI:

    def __init__(self, catalog_path: Path, out_dir: Path):
        self.catalog_path = catalog_path
        self.markdown_path = out_dir / "catalogs"
        self.parameter_guidline_path = out_dir / "parameters-guideline.json"
        self.catalog = Catalog.oscal_read(catalog_path)

    def generate_context(self, markdown_path):
        trestle_root: Path = None
        return ControlContext.generate(
            ContextPurpose.CATALOG,
            True,
            trestle_root,
            markdown_path,
            set_parameters_flag=True,
        )

    def generate_markdown(self) -> int:
        """Generate markdown for the controls in the catalog."""
        try:
            context = self.generate_context(self.markdown_path)
            catalog_api = CatalogAPI(catalog=self.catalog, context=context)
            catalog_api.write_catalog_as_markdown()

        except TrestleNotFoundError as e:
            raise TrestleError(f"Catalog {self.catalog_path} not found for load: {e}")
        except Exception as e:
            raise TrestleError(
                f"Error generating markdown for controls in {self.catalog_path}: {e}"
            )

        return CmdReturnCodes.SUCCESS.value

    def generate_parameter_guidline(self):
        guidelines = {}
        catalog_interface = CatalogInterface(self.catalog)
        for control in catalog_interface.get_all_controls_from_catalog(True):
            control_param_dict = ControlInterface.get_control_param_dict(control, False)
            for param_id, param in control_param_dict.items():
                guideline = self.generate_guideline(param_id, param)
                if param_id in guidelines:
                    logger.warning(
                        f"Duplicate param_id detected: '{param_id}' — skipping or overwriting previous guideline."
                    )
                else:
                    guidelines[param_id] = guideline
        with self.parameter_guidline_path.open("w") as f:
            json.dump(guidelines, f, indent=2, ensure_ascii=False)

    def generate_guideline(self, param_id: str, param: Parameter):

        guidelines = {
            "guideline": None,
            "aggregates": None,
            "alt-identifier": None,
            "select": None,
        }
        if param.guidelines and any(g.prose for g in param.guidelines):
            guidelines["guideline"] = "\n".join([g.prose for g in param.guidelines])

        props = {p.name: p.value for p in param.props}
        select = param.select

        if "aggregates" in props:
            aggregated = [p.value for p in param.props if p.name == "aggregates"]
            guidelines["aggregates"] = (
                f"represents a collection of values derived from the parameters: {', '.join(aggregated)}; "
                "when used in control text, values of each aggregated parameter should be substituted in place"
            )

        if "alt-identifier" in props:
            alt_id = props["alt-identifier"]
            guidelines["alt-identifier"] = (
                f"may also be referenced as '{alt_id}' in profiles or implementation layers"
            )
        if select:
            choices = select.choice
            how_many = select.how_many.value if select.how_many else "one"
            if how_many == "one":
                guideline = f"select exactly one of the following: {', '.join(choices)}"
            elif how_many == "one-or-more":
                guideline = f"select one or more from: {', '.join(choices)}"
            else:
                guideline = None
            guidelines["select"] = guideline

        if any([x for x in guidelines]):
            return self.stringify_guideline_fragments_natural(guidelines)
        else:
            logger.warning(
                (
                    f"No guideline generated for {param_id!r}: "
                    "parameter has no prose and does not match known structural patterns"
                    "(aggregates, alt-identifier, select). Consider reviewing manually. "
                    f"parameter_value={param.oscal_serialize_json()}"
                )
            )
            return f"no guideline is available for {param_id!r}."

    def stringify_guideline_fragments_natural(self, guidelines: dict[str, str]) -> str:
        fragments = [v.strip().rstrip(".") for v in guidelines.values() if v]
        return "\n".join(fragments)


def main():
    parser = argparse.ArgumentParser(
        description="Extract control statements from an OSCAL catalog (param-resolved)."
    )
    parser.add_argument(
        "-c",
        "--catalog",
        type=Path,
        required=True,
        help="Path to OSCAL catalog JSON file.",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        required=True,
        help="Output directory path for markdown files.",
    )
    args = parser.parse_args()

    cli = TrestleCLI(args.catalog, args.out)
    cli.generate_markdown()
    cli.generate_parameter_guidline()


if __name__ == "__main__":
    main()
