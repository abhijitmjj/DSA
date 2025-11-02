import pytest
from unittest import mock
import pathlib
import os

from azure.ai.ml import MLClient, Input, Output, command

# Removed Code from import
from azure.ai.ml.entities import Environment, PipelineJob, Command, Job
from azure.ai.ml.constants import AssetTypes
# If DefaultAzureCredential is used directly in the module, mock its import path
# from azure.identity import DefaultAzureCredential # Not mocking the import itself, but its instantiation

from utils.pipeline import Pipeline
from utils.pipeline_config import TargetSystem
from utils.commodity import Commodity  # Assuming this enum exists and is importable

MOCK_CONFIG_PATH = "/fake/path/to/config.json"


@pytest.fixture
def mock_default_azure_credential(mocker):
    """Mocks DefaultAzureCredential instantiation."""
    return mocker.patch("utils.pipeline.DefaultAzureCredential", autospec=True)


@pytest.fixture
def mock_ml_client_constructor(mocker):
    """Mocks the MLClient class constructor itself."""
    return mocker.patch("utils.pipeline.MLClient", autospec=True)


@pytest.fixture
def mock_ml_client_from_config(mocker):
    """Mocks MLClient.from_config static method."""
    mock_client_instance = mock.MagicMock(spec=MLClient)
    mock_client_instance.workspace_name = "mock_workspace"
    # Mock other attributes/methods of MLClient instance if needed by Pipeline.__init__
    mock_client_instance.compute.get.return_value = (
        mock.MagicMock()
    )  # for _get_or_create_compute_target
    mock_client_instance.environments.get.return_value = mock.MagicMock(
        spec=Environment
    )  # for _get_default_environment

    mock_from_config = mocker.patch(
        "utils.pipeline.MLClient.from_config", return_value=mock_client_instance
    )
    return mock_from_config, mock_client_instance


@pytest.fixture
def minimal_pipeline_params():
    """Provides minimal parameters for Pipeline initialization."""
    return {
        "target_system": TargetSystem.DEV,
        "config_file": MOCK_CONFIG_PATH,
        "cluster_name": "test-cluster",
        "datastore_name": "test_datastore",
    }


@pytest.fixture
def mock_command_func(mocker):
    """Mocks the azure.ai.ml.command function."""
    component_factory_mock = mocker.MagicMock(spec=Command)

    node_instance = Command(
        name="mock_node",
        command="echo mock_node",
        environment="AzureML-Minimal:1",
        code=".",  # Use "." for code path
        component=component_factory_mock,
    )
    component_factory_mock.return_value = node_instance

    return mocker.patch("utils.pipeline.command", return_value=component_factory_mock)


@pytest.fixture
def pipeline_instance(
    mocker,
    mock_default_azure_credential,
    mock_ml_client_from_config,
    minimal_pipeline_params,
):
    """Provides a Pipeline instance with a mocked ml_client for testing other methods."""
    mocker.patch("pathlib.Path.resolve", return_value=pathlib.Path(MOCK_CONFIG_PATH))
    mocker.patch("pathlib.Path.is_file", return_value=True)

    # Mock _get_or_create_compute_target and _get_default_environment for this fixture
    mocker.patch(
        "utils.pipeline.Pipeline._get_or_create_compute_target",
        return_value="test-cluster",
    )
    # _get_default_environment returns an Environment object
    mock_env = mock.MagicMock(spec=Environment)
    mocker.patch(
        "utils.pipeline.Pipeline._get_default_environment", return_value=mock_env
    )

    return Pipeline(**minimal_pipeline_params)


class TestPipelineInitialization:
    def test_init_success_with_specific_config_file(
        self,
        mocker,
        mock_default_azure_credential,
        mock_ml_client_from_config,
        minimal_pipeline_params,
    ):
        """Tests successful initialization when a specific config file is found and used."""
        mocker.patch(
            "pathlib.Path.resolve", return_value=pathlib.Path(MOCK_CONFIG_PATH)
        )
        mocker.patch("pathlib.Path.is_file", return_value=True)

        mock_from_config, _ = mock_ml_client_from_config

        pipeline = Pipeline(**minimal_pipeline_params)

        mock_default_azure_credential.assert_called_once()
        mock_from_config.assert_called_once_with(
            credential=mock_default_azure_credential.return_value, path=MOCK_CONFIG_PATH
        )
        assert pipeline.ml_client is not None
        assert pipeline.ml_client.workspace_name == "mock_workspace"
        assert pipeline._config_file == MOCK_CONFIG_PATH

    def test_init_success_with_default_config_file(
        self,
        mocker,
        mock_default_azure_credential,
        mock_ml_client_from_config,
        minimal_pipeline_params,
    ):
        """Tests successful initialization when specific config is not found, uses default."""

        # New mocking strategy for pathlib.Path interactions
        # 1. Mock for the object returned by resolve()
        mock_resolved_path = mock.MagicMock(spec=pathlib.Path)
        mock_resolved_path.is_file.return_value = False  # This is crucial
        # Ensure it can be cast to str if the if-branch were taken (not expected here)
        mock_resolved_path.__str__ = mock.Mock(return_value=MOCK_CONFIG_PATH)

        # 2. Mock for the initial Path object created by pathlib.Path(self._config_file)
        mock_initial_path = mock.MagicMock(spec=pathlib.Path)
        mock_initial_path.resolve.return_value = mock_resolved_path

        # 3. Mock the Path constructor as used in utils.pipeline.pathlib.Path
        # This ensures that when `pathlib.Path(...)` is called in pipeline.py, it returns our mock_initial_path
        mocker.patch("utils.pipeline.pathlib.Path", return_value=mock_initial_path)

        mock_from_config, _ = mock_ml_client_from_config

        pipeline = Pipeline(**minimal_pipeline_params)

        # Assert that utils.pipeline.pathlib.Path was called with the config file path
        # This confirms our mock constructor was engaged.
        # The actual call to pathlib.Path() happens inside the Pipeline constructor.
        # We need to ensure it was called with self._config_file (MOCK_CONFIG_PATH)
        # Example: utils.pipeline.pathlib.Path.assert_called_once_with(MOCK_CONFIG_PATH)
        # This needs `mocker.patch('utils.pipeline.pathlib.Path')` to be the Patched object, not just return_value.
        # For simplicity, the current mock setup with return_value is fine if we trust it's called.
        # The key is that mock_resolved_path.is_file.return_value = False takes effect.

        mock_default_azure_credential.assert_called_once()

        # MLClient.from_config should be called once (for the default lookup)
        mock_from_config.assert_called_once_with(
            credential=mock_default_azure_credential.return_value
        )

        assert pipeline.ml_client is not None
        assert pipeline.ml_client.workspace_name == "mock_workspace"

    def test_init_success_with_env_vars(
        self,
        mocker,
        mock_default_azure_credential,
        mock_ml_client_constructor,
        minimal_pipeline_params,
    ):
        """Tests successful initialization using environment variables when config files fail."""
        mocker.patch(
            "pathlib.Path.resolve", return_value=pathlib.Path(MOCK_CONFIG_PATH)
        )
        mocker.patch(
            "pathlib.Path.is_file", return_value=False
        )  # Specific config file not found

        # Make MLClient.from_config raise an exception to trigger env var fallback
        mocker.patch(
            "utils.pipeline.MLClient.from_config",
            side_effect=Exception("Config load failed"),
        )

        mock_env = {
            "AZURE_SUBSCRIPTION_ID": "test_sub",
            "AZURE_RESOURCE_GROUP": "test_rg",
            "AZURE_WORKSPACE_NAME": "test_ws_env",
        }
        mocker.patch.dict(os.environ, mock_env)

        # Mock the MLClient instance that would be created by the constructor
        mock_ml_client_instance_env = mock.MagicMock(spec=MLClient)
        mock_ml_client_instance_env.workspace_name = "test_ws_env"
        mock_ml_client_instance_env.compute.get.return_value = mock.MagicMock()
        mock_ml_client_instance_env.environments.get.return_value = mock.MagicMock(
            spec=Environment
        )
        mock_ml_client_constructor.return_value = mock_ml_client_instance_env

        pipeline = Pipeline(**minimal_pipeline_params)

        mock_default_azure_credential.assert_called_once()
        mock_ml_client_constructor.assert_called_once_with(
            credential=mock_default_azure_credential.return_value,
            subscription_id="test_sub",
            resource_group_name="test_rg",
            workspace_name="test_ws_env",
        )
        assert pipeline.ml_client is not None
        assert pipeline.ml_client.workspace_name == "test_ws_env"

    def test_init_failure_no_config_or_env_vars(
        self, mocker, mock_default_azure_credential, minimal_pipeline_params
    ):
        """Tests Pipeline initialization failure when no config files or env vars are found."""
        mocker.patch(
            "pathlib.Path.resolve", return_value=pathlib.Path(MOCK_CONFIG_PATH)
        )
        mocker.patch("pathlib.Path.is_file", return_value=False)
        mocker.patch(
            "utils.pipeline.MLClient.from_config",
            side_effect=Exception("Config load failed"),
        )
        mocker.patch.dict(os.environ, {}, clear=True)  # Ensure no relevant env vars

        # Match the exact error message raised by Pipeline.__init__
        expected_error_msg = "PIPELINE_INIT_ERROR: Azure ML workspace configuration not found in config file or environment variables."
        with pytest.raises(ValueError, match=expected_error_msg):
            Pipeline(**minimal_pipeline_params)

        mock_default_azure_credential.assert_called_once()

    def test_init_compute_and_env_creation_mocked(
        self,
        mocker,
        mock_default_azure_credential,
        mock_ml_client_from_config,
        minimal_pipeline_params,
    ):
        """Tests that compute and environment methods are called on ml_client during init."""
        mocker.patch(
            "pathlib.Path.resolve", return_value=pathlib.Path(MOCK_CONFIG_PATH)
        )
        mocker.patch("pathlib.Path.is_file", return_value=True)

        _, mock_client_instance = mock_ml_client_from_config

        # Mock the internal methods of Pipeline that get called
        mock_get_compute = mocker.patch(
            "utils.pipeline.Pipeline._get_or_create_compute_target",
            return_value="test-cluster",
        )
        # We also need to mock _get_default_environment because it's called by add_step,
        # but for init, it's not directly called. However, the mock_client_instance needs its env part mocked.
        # The _get_or_create_compute_target is called in __init__.

        pipeline = Pipeline(**minimal_pipeline_params)

        mock_get_compute.assert_called_once_with(cluster_name="test-cluster")
        assert pipeline._compute_target == "test-cluster"
        # _get_default_environment is not called during __init__
        # pipeline.ml_client.environments.get would be called by _get_default_environment if that was tested here.


class TestPipelineStepManagement:
    def test_add_simple_step(self, pipeline_instance, mock_command_func):
        """Tests adding a basic step without specific inputs/outputs."""
        script_path = "steps/train.py"
        step_name = "train_step"

        pipeline_instance.add_step(name=step_name, script_path=script_path)

        mock_command_func.assert_called_once()
        args, kwargs = mock_command_func.call_args
        assert kwargs["name"] == step_name
        assert kwargs["command"] == f"python {pathlib.Path(script_path).name}"
        assert "inputs" in kwargs
        assert "outputs" in kwargs
        assert kwargs["code"] == str(pipeline_instance._project_root / "steps")
        assert kwargs["compute"] == "test-cluster"
        assert isinstance(
            kwargs["environment"], mock.MagicMock
        )  # From _get_default_environment mock

        assert step_name in pipeline_instance._step_definitions
        component_factory, defined_inputs = pipeline_instance._step_definitions[
            step_name
        ]
        assert component_factory is mock_command_func.return_value  # The factory itself
        assert defined_inputs == {}

    def test_add_step_with_inputs_outputs(self, pipeline_instance, mock_command_func):
        """Tests adding a step with defined inputs and outputs."""
        script_path = "steps/process.py"
        step_name = "process_step"
        inputs = {"raw_data": Input(type=AssetTypes.URI_FILE, path="/test/data.csv")}
        outputs = {
            "processed_data": Output(
                type=AssetTypes.URI_FOLDER, path="/test/processed/"
            )
        }

        pipeline_instance.add_step(
            name=step_name, script_path=script_path, inputs=inputs, outputs=outputs
        )

        mock_command_func.assert_called_once()
        args, kwargs = mock_command_func.call_args
        assert kwargs["name"] == step_name
        assert kwargs["inputs"] == inputs
        assert kwargs["outputs"] == outputs

        assert step_name in pipeline_instance._step_definitions
        component_factory, defined_inputs = pipeline_instance._step_definitions[
            step_name
        ]
        assert component_factory is mock_command_func.return_value
        assert defined_inputs == inputs
        assert step_name in pipeline_instance._step_outputs
        assert pipeline_instance._step_outputs[step_name] == outputs

    def test_get_output_success(self, pipeline_instance, mock_command_func):
        """Tests successfully retrieving an output definition for use as an input."""
        script_path = "steps/producer.py"
        step_name = "producer_step"
        output_name = "produced_data"
        outputs = {
            output_name: Output(type=AssetTypes.URI_FOLDER, path="/test/produced/")
        }

        pipeline_instance.add_step(
            name=step_name, script_path=script_path, outputs=outputs
        )

        input_for_next_step = pipeline_instance.get_output(step_name, output_name)

        assert isinstance(input_for_next_step, Input)
        assert input_for_next_step.type == AssetTypes.URI_FOLDER
        assert (
            input_for_next_step.path
            == f"${{{{parent.jobs.{step_name}.outputs.{output_name}}}}}"
        )

    def test_get_output_not_found(self, pipeline_instance):
        """Tests attempting to get an output that does not exist."""
        result = pipeline_instance.get_output("non_existent_step", "some_output")
        assert result is None


class TestPipelineSubmission:
    def test_submit_no_steps(self, pipeline_instance):
        """Tests that submitting a pipeline with no steps raises ValueError."""
        with pytest.raises(ValueError, match="No step definitions added"):
            pipeline_instance.submit(experiment_name="test_experiment")

    def test_submit_single_step(self, pipeline_instance, mock_command_func):
        """Tests submitting a pipeline with a single step."""
        script_path = "steps/train.py"
        step_name = "train_step"  # Fixed unterminated string literal

        # The mock_command_func returns a factory (mock_component_factory).
        # When this factory is called (component_factory(**defined_inputs)), it returns a node (mock_node).
        mock_component_factory = mock_command_func.return_value
        mock_node = mock_component_factory.return_value  # This is the Job-like object

        pipeline_instance.add_step(name=step_name, script_path=script_path)

        mock_job_operations = pipeline_instance.ml_client.jobs
        mock_submitted_job = mock.MagicMock(spec=PipelineJob)
        mock_job_operations.create_or_update.return_value = mock_submitted_job

        submitted_job = pipeline_instance.submit(experiment_name="test_experiment")

        # Assert that the component factory was called to create the node
        mock_component_factory.assert_called_once_with()  # Called with no inputs in this simple case

        mock_job_operations.create_or_update.assert_called_once()
        args, kwargs = mock_job_operations.create_or_update.call_args
        pipeline_job_arg = args[0]
        assert isinstance(pipeline_job_arg, PipelineJob)
        assert pipeline_job_arg.experiment_name == "test_experiment"
        assert pipeline_job_arg.compute == "test-cluster"
        assert len(pipeline_job_arg.jobs) == 1
        assert (
            pipeline_job_arg.jobs[step_name] is mock_node
        )  # Check the node is in the job
        assert submitted_job is mock_submitted_job

    def test_submit_multi_step_with_dependency(
        self, pipeline_instance, mock_command_func
    ):
        """Tests submitting a pipeline with two steps where one depends on the other."""
        producer_script = "steps/producer.py"
        producer_step_name = "producer"
        producer_output_name = "data_out"
        producer_outputs = {producer_output_name: Output(type=AssetTypes.URI_FOLDER)}

        producer_component_factory = mock.MagicMock(spec=Command)
        producer_node_instance = Command(
            name="producer_node",
            command="echo producer",
            environment="AzureML-Minimal:1",
            code=".",  # Use "." for code path
            component=producer_component_factory,
        )
        producer_component_factory.return_value = producer_node_instance

        consumer_component_factory = mock.MagicMock(spec=Command)
        consumer_node_instance = Command(
            name="consumer_node",
            command="echo consumer",
            environment="AzureML-Minimal:1",
            code=".",  # Use "." for code path
            component=consumer_component_factory,
        )
        consumer_component_factory.return_value = consumer_node_instance

        mock_command_func.side_effect = [
            producer_component_factory,
            consumer_component_factory,
        ]

        pipeline_instance.add_step(
            name=producer_step_name,
            script_path=producer_script,
            outputs=producer_outputs,
        )

        # Step 2: Consumer
        consumer_script = "steps/consumer.py"
        consumer_step_name = "consumer"
        consumer_input_name = "data_in"
        consumer_inputs = {
            consumer_input_name: pipeline_instance.get_output(
                producer_step_name, producer_output_name
            )
        }
        pipeline_instance.add_step(
            name=consumer_step_name, script_path=consumer_script, inputs=consumer_inputs
        )

        mock_job_operations = pipeline_instance.ml_client.jobs
        mock_submitted_job = mock.MagicMock(spec=PipelineJob)
        mock_job_operations.create_or_update.return_value = mock_submitted_job

        submitted_job = pipeline_instance.submit(experiment_name="multi_step_exp")

        # Assert producer component factory was called
        producer_component_factory.assert_called_once_with()  # Assuming no inputs for producer in this setup
        # Assert consumer component factory was called with its defined inputs
        consumer_component_factory.assert_called_once_with(**consumer_inputs)

        mock_job_operations.create_or_update.assert_called_once()
        pipeline_job_arg = mock_job_operations.create_or_update.call_args[0][0]
        assert isinstance(pipeline_job_arg, PipelineJob)
        assert len(pipeline_job_arg.jobs) == 2
        assert pipeline_job_arg.jobs[producer_step_name] is producer_node_instance
        assert pipeline_job_arg.jobs[consumer_step_name] is consumer_node_instance
        assert submitted_job is mock_submitted_job


class TestPipelineCommodityInstantiation:
    @pytest.mark.parametrize(
        "commodity_obj, expected_log_part",
        [
            (Commodity.SOYMEAL, "Soymeal"),
            (Commodity.OILCOMPLEX_PALM, "Oilcomplex Palm"),
            (None, "None"),
        ],
    )
    def test_pipeline_instantiation_with_commodities(
        self,
        mocker,
        mock_default_azure_credential,
        mock_ml_client_from_config,
        minimal_pipeline_params,
        commodity_obj,
        expected_log_part,
    ):
        """Tests Pipeline instantiation with different commodity types (mostly for attribute check)."""
        mocker.patch(
            "pathlib.Path.resolve", return_value=pathlib.Path(MOCK_CONFIG_PATH)
        )
        mocker.patch("pathlib.Path.is_file", return_value=True)
        mocker.patch("utils.pipeline.Pipeline._get_or_create_compute_target")
        mocker.patch("utils.pipeline.Pipeline._get_default_environment")

        params = {**minimal_pipeline_params, "commodity": commodity_obj}
        pipeline = Pipeline(**params)
        assert pipeline.commodity == commodity_obj
        # This test mainly verifies the commodity attribute is set.
        # If commodity had specific logic in Pipeline, more detailed checks would be needed.
