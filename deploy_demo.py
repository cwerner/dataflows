import os

from prefect.deployments import Deployment
from prefect.packaging.file import FilePackager
from prefect.filesystems import RemoteFileSystem
from prefect.flow_runners import KubernetesFlowRunner

from dotenv import load_dotenv

class EnvVarMissingError(Exception):
    pass

load_dotenv()


AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY", None)
ENDPOINT_URL=os.environ.get("ENDPOINT_URL", "https://s3.imk-ifu.kit.edu:10443")

if not AWS_ACCESS_KEY_ID:
    raise EnvVarMissingError
if not AWS_SECRET_ACCESS_KEY:
    raise EnvVarMissingError


storagegrid_file_packager = FilePackager(
    filesystem=RemoteFileSystem(
        basepath="s3://dataflows",
        settings={
            "key": AWS_ACCESS_KEY_ID,
            "secret": AWS_SECRET_ACCESS_KEY,
            "client_kwargs": {"endpoint_url": ENDPOINT_URL}
        }
    )
)

Deployment(
    flow="./flow_demo.py",
    flow_runner=KubernetesFlowRunner(stream_output=True),
    #tags=['demo'],
    name="storagegrid_file_package_with_remote_s3fs",
    packager=storagegrid_file_packager
)
