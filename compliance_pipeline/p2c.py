import argparse
from pathlib import Path

import yaml

from c2p.framework.c2p import C2P
from c2p.framework.models import RawResult
from c2p.framework.models.c2p_config import C2PConfig, ComplianceOscal
from c2p.framework.models.raw_result import RawResult

from compliance_pipeline.c2p_plugin.kyverno import PluginKyverno

parser = argparse.ArgumentParser()
parser.add_argument(
    '-polr',
    '--policy-report',
    type=str,
    help='Path to policy report',
    required=False,
)
parser.add_argument(
    '-c',
    '--component_definition',
    type=str,
    help=f'Path to component-definition.json',
    required=False,
)
args = parser.parse_args()

base_dir = Path(__file__).parent
policy_template_dir = f'{base_dir.absolute().as_posix()}/c2p_plugin/policy-resources'

# Setup c2p_config
c2p_config = C2PConfig()
c2p_config.compliance = ComplianceOscal()
c2p_config.compliance.component_definition = args.component_definition
c2p_config.pvp_name = 'Kyverno'
c2p_config.result_title = 'Kyverno Assessment Results'
c2p_config.result_description = 'OSCAL Assessment Results from Kyverno'

# Construct C2P
c2p = C2P(c2p_config)

# Create pvp_result from raw result via plugin
polr = yaml.safe_load(Path(args.policy_report).open('r'))
pvp_raw_result = RawResult(data=polr['items'])
pvp_result = PluginKyverno().generate_pvp_result(pvp_raw_result)

# Transform pvp_result to OSCAL Assessment Result
c2p.set_pvp_result(pvp_result)
oscal_assessment_results = c2p.result_to_oscal()

print(oscal_assessment_results.oscal_serialize_json(pretty=True))
