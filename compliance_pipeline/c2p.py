import argparse
import os
from pathlib import Path
import sys
import tempfile

from c2p.framework.c2p import C2P
from c2p.framework.models.c2p_config import C2PConfig, ComplianceOscal

from compliance_pipeline.c2p_plugin.kyverno import PluginConfigKyverno, PluginKyverno

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c',
    '--component_definition',
    type=str,
    help=f'Path to component-definition.json',
    required=True,
)
parser.add_argument(
    '-o', '--out', type=str, help='Path to output directory (default: system temporary directory)', required=False
)
args = parser.parse_args()

tmpdirname = args.out if args.out != None else tempfile.mkdtemp()

# Setup c2p_config
c2p_config = C2PConfig()
c2p_config.compliance = ComplianceOscal()
c2p_config.compliance.component_definition = args.component_definition
c2p_config.pvp_name = 'Kyverno'
c2p_config.result_title = 'Kyverno Assessment Results'
c2p_config.result_description = 'OSCAL Assessment Results from Kyverno'

# Construct C2P
c2p = C2P(c2p_config)

# Transform OSCAL (Compliance) to Policy
base_dir = Path(__file__).parent
policy_template_dir = f'{base_dir.absolute().as_posix()}/c2p_plugin/policy-resources'
config = PluginConfigKyverno(policy_template_dir=policy_template_dir, deliverable_policy_dir=tmpdirname)
PluginKyverno(config).generate_pvp_policy(c2p.get_policy())


def tree(path: Path, texts: list[str] = [], depth=0) -> list[str]:
    prefix = ''
    if depth > 0:
        for _ in range(depth):
            prefix = prefix + '-'
        prefix = prefix + ' '
    for item in path.iterdir():
        texts.append(f'{prefix}{item.name}')
        if item.is_dir():
            tree(item, texts, depth=depth + 1)
    return texts


print('')
print(f'tree {tmpdirname}')
for text in tree(Path(tmpdirname)):
    print(text)
