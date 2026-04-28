# OUTPUT - test

## Demo for the retry-with-backoff prototype added to Otter

Otter is a YAML-driven task execution framework used in the Open Targets data pipeline. It already supports YAML-defined steps, parallel task execution, logging, and a manifest for tracking execution and provenance. In the original behavior, if a task fails, Otter stops the pipeline and records the failure in the manifest. This prototype changes that behavior for retryable failures by retrying the failing phase before the task is marked as failed. 


Thought of design -- [DESIGN.md](../DESIGN.md).

## Setup

- Start from the [PIS]() repo:

    ```bash
    uv sync
    ```

    `uv sync` updates the project environment from the lockfile, while `uv run` also locks and syncs automatically before running the command. I still ran `uv sync` first so the environment was ready before the demo.



    **Keep [Otter]() and [PIS]() under the same parent directory so [PIS]() can use the revised local [Otter]() package.**

- Run the local flaky server in one terminal:

    ```
    python3 flaky_server.py
    ```
    - What does flaky_server.py do here?
        It acts as a tiny local test endpoint for the copy task.
    
    - For this demo, the server is designed to:

        1. return 503 Service Unavailable for the first two requests
        2. return a normal successful response on the third request
        3. support validation of the downloaded file afterward

        --> make the failure deterministic, so the retry behavior can be tested in a controlled way instead of waiting for a real remote service to fail at the right moment.


- Run the demo step in another terminal:

    ```
    uv run pis -s retry_demo
    ```

    - **What was added in retry_demo?**

        A small demo step was added to config.yaml:
        ``` yaml
        steps:
          retry_demo:
            - name: copy flaky demo
              source: http://127.0.0.1:8000/flaky.json
              destination: input/retry_demo/flaky.json
              retry:
                max_attempts: 3
                initial_delay_seconds: 1
                backoff: exponential
                max_delay_seconds: 10
                jitter: false
        ```


## Actual Output

Below is the actual behavior from the demo run:

    1. the task starts running
    2. the first run() attempt fails with 503
    3. Otter classifies it as retryable and waits 1 second
    4. the second run() attempt fails with 503
    5. Otter classifies it as retryable again and waits 2 seconds
    6. the third run() attempt succeeds
    7. validation then runs and succeeds
    8. the whole retry_demo step completes successfully

```
uv run pis -s retry_demo

/Users/apple/Desktop/Projects/opensource/pis/.venv/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (6.0.0.post1)/charset_normalizer (3.4.4) doesn't match a supported version!
  warnings.warn(
2026-04-29 05:54:34.755 | M:73739  | DEBUG    | otter.util.logger:init_logger_early:168 - early logger configured
2026-04-29 05:54:34.756 | M:73739  | DEBUG    | otter.config.env:parse_env:26 - parsing environment variables
2026-04-29 05:54:34.756 | M:73739  | DEBUG    | otter.config.cli:parse_cli:30 - parsing cli arguments
2026-04-29 05:54:34.757 | M:73739  | DEBUG    | otter.config.yaml:parse_yaml:30 - loading yaml file /Users/apple/Desktop/Projects/opensource/pis/config.yaml
2026-04-29 05:54:34.796 | M:73739  | TRACE    | otter.config:load_config:76 - loaded settings: runner_name='pis' step='retry_demo' steps=['retry_demo', 'biosample', 'baseline_expression', 'clinical_report', 'disease', 'drug', 'impc', 'evidence_expression_atlas', 'evidence_cancer_biomarkers', 'evidence_clingen', 'evidence_cosmic', 'evidence_project_score', 'evidence_crispr_screens', 'evidence_eva', 'evidence_gene_burden', 'evidence_gene2phenotype', 'evidence_panel_app', 'evidence_orphanet', 'evidence_reactome', 'evidence_uniprot_literature', 'evidence_uniprot_variants', 'evidence_intogen', 'evidence_ppp', 'expression', 'go', 'interaction', 'encode', 'gwas', 'gwas_ppp', 'l2g', 'literature', 'molqtl', 'molqtl_ppp', 'ontoma', 'openfda', 'otar', 'pharmacogenetics', 'reactome', 'so', 'target', 'target_prioritisation'] config_path=PosixPath('/Users/apple/Desktop/Projects/opensource/pis/config.yaml') work_path=PosixPath('/Users/apple/Desktop/Projects/opensource/pipeline_work') release_uri=None pool_size=2 log_level='DEBUG'
2026-04-29 05:54:34.796 | M:73739  | INFO     | otter.config:load_config:78 - no release uri provided, run is local
2026-04-29 05:54:34.804 | M:73739  | DEBUG    | otter.util.logger:init_logger:188 - logger configured, level DEBUG
2026-04-29 05:54:34.804 | M:73739  | INFO     | otter.core:__init__:49 - otter v26.3.5 starting!
2026-04-29 05:54:34.807 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type copy
2026-04-29 05:54:34.808 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type copy_many
2026-04-29 05:54:34.809 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type download
2026-04-29 05:54:34.810 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type explode
2026-04-29 05:54:34.811 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type explode_glob
2026-04-29 05:54:34.812 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type find_latest
2026-04-29 05:54:34.813 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type hello_world
2026-04-29 05:54:34.814 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type crawl_encode
2026-04-29 05:54:34.815 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type crispr_brain
2026-04-29 05:54:34.840 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type elasticsearch
2026-04-29 05:54:34.844 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type explode_openfda
2026-04-29 05:54:34.845 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type panel_app
2026-04-29 05:54:34.846 | M:73739  | DEBUG    | otter.task.task_registry:register:81 - registered task type solr
/Users/apple/Desktop/Projects/opensource/pis/.venv/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (6.0.0.post1)/charset_normalizer (3.4.4) doesn't match a supported version!
  warnings.warn(
2026-04-29 05:54:35.437 | M:73739  | INFO     | otter.step.coordinator:run:256 - starting coordinator for step: retry_demo
2026-04-29 05:54:35.437 | M:73739  | INFO     | otter.step.model:start:35 - step retry_demo started running
2026-04-29 05:54:35.437 | M:73739  | INFO     | otter.step.coordinator:_start_workers:219 - starting 2 worker processes
2026-04-29 05:54:35.440 | M:73739  | DEBUG    | otter.step.coordinator:_start_workers:232 - started worker 0 (pid=73742)
2026-04-29 05:54:35.446 | M:73739  | DEBUG    | otter.step.coordinator:_start_workers:232 - started worker 1 (pid=73743)
2026-04-29 05:54:35.449 | M:73739  | DEBUG    | otter.step.coordinator:_build_spec_into_task:88 - building task for spec copy flaky demo
2026-04-29 05:54:35.450 | M:73739  | DEBUG    | otter.task.model:__init__:167 - initialized task copy flaky demo
2026-04-29 05:54:35.450 | M:73739  | DEBUG    | otter.step.coordinator:_enqueue_tasks:105 - enqueuing task copy flaky demo
/Users/apple/Desktop/Projects/opensource/pis/.venv/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (6.0.0.post1)/charset_normalizer (3.4.4) doesn't match a supported version!
  warnings.warn(
/Users/apple/Desktop/Projects/opensource/pis/.venv/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (6.0.0.post1)/charset_normalizer (3.4.4) doesn't match a supported version!
  warnings.warn(
2026-04-29 05:54:35.830 | INFO     | otter.step.worker:run:61 - worker 1 started
2026-04-29 05:54:35.832 | INFO     | otter.step.worker:run:70 - worker 1 executing task copy flaky demo
2026-04-29 05:54:35.832 | INFO     | otter.step.worker:run:61 - worker 0 started
2026-04-29 05:54:35.836 | DEBUG    | otter.util.logger:task_logging:121 - added missing stdout logger
2026-04-29 05:54:35.836 | W:73743  | DEBUG    | otter.util.logger:task_logging:121 - added missing stdout logger
2026-04-29 05:54:35.839 | DEBUG    | otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.run of <otter.tasks.copy.Copy object at 0x111336d10>> wrapped_func=<function Copy.run at 0x11134c220> raw_func=<function Copy.run at 0x11134c040> method_name=run raw_name=run
2026-04-29 05:54:35.839 | W:73743  | DEBUG    | copy flaky demo::otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.run of <otter.tasks.copy.Copy object at 0x111336d10>> wrapped_func=<function Copy.run at 0x11134c220> raw_func=<function Copy.run at 0x11134c040> method_name=run raw_name=run
2026-04-29 05:54:35.840 | INFO     | otter.tasks.copy:run:43 - copying file from http://127.0.0.1:8000/flaky.json to input/retry_demo/flaky.json
2026-04-29 05:54:35.840 | W:73743  | INFO     | copy flaky demo::otter.tasks.copy:run:43 - copying file from http://127.0.0.1:8000/flaky.json to input/retry_demo/flaky.json
2026-04-29 05:54:35.840 | DEBUG    | otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:35.840 | W:73743  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:35.840 | DEBUG    | otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:35.840 | W:73743  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:35.848 | WARNING  | otter.step.worker:execute_task:131 - task=copy flaky demo phase=run attempt=1/3 retryable=True next_delay_s=1 error=HTTPError: 503 Server Error: Service Unavailable for url: http://127.0.0.1:8000/flaky.json
2026-04-29 05:54:35.848 | W:73743  | WARNING  | copy flaky demo::otter.step.worker:execute_task:131 - task=copy flaky demo phase=run attempt=1/3 retryable=True next_delay_s=1 error=HTTPError: 503 Server Error: Service Unavailable for url: http://127.0.0.1:8000/flaky.json
2026-04-29 05:54:36.851 | DEBUG    | otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.run of <otter.tasks.copy.Copy object at 0x111336d10>> wrapped_func=<function Copy.run at 0x11134c220> raw_func=<function Copy.run at 0x11134c040> method_name=run raw_name=run
2026-04-29 05:54:36.851 | W:73743  | DEBUG    | copy flaky demo::otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.run of <otter.tasks.copy.Copy object at 0x111336d10>> wrapped_func=<function Copy.run at 0x11134c220> raw_func=<function Copy.run at 0x11134c040> method_name=run raw_name=run
2026-04-29 05:54:36.851 | INFO     | otter.tasks.copy:run:43 - copying file from http://127.0.0.1:8000/flaky.json to input/retry_demo/flaky.json
2026-04-29 05:54:36.851 | W:73743  | INFO     | copy flaky demo::otter.tasks.copy:run:43 - copying file from http://127.0.0.1:8000/flaky.json to input/retry_demo/flaky.json
2026-04-29 05:54:36.851 | DEBUG    | otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:36.851 | W:73743  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:36.851 | DEBUG    | otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:36.851 | W:73743  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:36.854 | WARNING  | otter.step.worker:execute_task:131 - task=copy flaky demo phase=run attempt=2/3 retryable=True next_delay_s=2 error=HTTPError: 503 Server Error: Service Unavailable for url: http://127.0.0.1:8000/flaky.json
2026-04-29 05:54:36.854 | W:73743  | WARNING  | copy flaky demo::otter.step.worker:execute_task:131 - task=copy flaky demo phase=run attempt=2/3 retryable=True next_delay_s=2 error=HTTPError: 503 Server Error: Service Unavailable for url: http://127.0.0.1:8000/flaky.json
2026-04-29 05:54:38.859 | DEBUG    | otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.run of <otter.tasks.copy.Copy object at 0x111336d10>> wrapped_func=<function Copy.run at 0x11134c220> raw_func=<function Copy.run at 0x11134c040> method_name=run raw_name=run
2026-04-29 05:54:38.859 | W:73743  | DEBUG    | copy flaky demo::otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.run of <otter.tasks.copy.Copy object at 0x111336d10>> wrapped_func=<function Copy.run at 0x11134c220> raw_func=<function Copy.run at 0x11134c040> method_name=run raw_name=run
2026-04-29 05:54:38.860 | INFO     | otter.tasks.copy:run:43 - copying file from http://127.0.0.1:8000/flaky.json to input/retry_demo/flaky.json
2026-04-29 05:54:38.860 | W:73743  | INFO     | copy flaky demo::otter.tasks.copy:run:43 - copying file from http://127.0.0.1:8000/flaky.json to input/retry_demo/flaky.json
2026-04-29 05:54:38.860 | DEBUG    | otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:38.860 | W:73743  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:38.861 | DEBUG    | otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:38.861 | W:73743  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:38.867 | SUCCESS  | otter.step.worker:execute_task:107 - task=copy flaky demo phase=run attempt=3/3 event=success
2026-04-29 05:54:38.867 | W:73743  | SUCCESS  | copy flaky demo::otter.step.worker:execute_task:107 - task=copy flaky demo phase=run attempt=3/3 event=success
2026-04-29 05:54:38.868 | INFO     | otter.step.worker:run:75 - worker 1 completed task copy flaky demo
2026-04-29 05:54:38.868 | W:73743  | INFO     | otter.step.worker:run:75 - worker 1 completed task copy flaky demo
2026-04-29 05:54:38.976 | M:73739  | INFO     | otter.scratchpad.model:merge:97 - added 0 new entries to scratchpad
2026-04-29 05:54:38.976 | M:73739  | DEBUG    | otter.step.coordinator:_enqueue_tasks:105 - enqueuing task copy flaky demo
2026-04-29 05:54:38.979 | INFO     | otter.step.worker:run:70 - worker 0 executing task copy flaky demo
2026-04-29 05:54:38.986 | DEBUG    | otter.util.logger:task_logging:121 - added missing stdout logger
2026-04-29 05:54:38.986 | W:73742  | DEBUG    | otter.util.logger:task_logging:121 - added missing stdout logger
2026-04-29 05:54:38.992 | DEBUG    | otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.validate of <otter.tasks.copy.Copy object at 0x11a13b3d0>> wrapped_func=<function Copy.validate at 0x11a14c360> raw_func=<function Copy.validate at 0x11a14c180> method_name=validate raw_name=validate
2026-04-29 05:54:38.992 | W:73742  | DEBUG    | copy flaky demo::otter.step.worker:_call_unwrapped:211 - method=<bound method Copy.validate of <otter.tasks.copy.Copy object at 0x11a13b3d0>> wrapped_func=<function Copy.validate at 0x11a14c360> raw_func=<function Copy.validate at 0x11a14c180> method_name=validate raw_name=validate
2026-04-29 05:54:38.992 | DEBUG    | otter.validators.file:exists:56 - checking if file exists: input/retry_demo/flaky.json
2026-04-29 05:54:38.992 | W:73742  | DEBUG    | copy flaky demo::otter.validators.file:exists:56 - checking if file exists: input/retry_demo/flaky.json
2026-04-29 05:54:38.992 | DEBUG    | otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:38.992 | W:73742  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:38.992 | W:73742  | TRACE    | copy flaky demo::otter.validators.file:exists:60 - file input/retry_demo/flaky.json exists
2026-04-29 05:54:38.992 | DEBUG    | otter.validators.file:size:141 - checking if http://127.0.0.1:8000/flaky.json and input/retry_demo/flaky.json are the same size
2026-04-29 05:54:38.992 | W:73742  | DEBUG    | copy flaky demo::otter.validators.file:size:141 - checking if http://127.0.0.1:8000/flaky.json and input/retry_demo/flaky.json are the same size
2026-04-29 05:54:38.992 | DEBUG    | otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:38.992 | W:73742  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:72 - location http://127.0.0.1:8000/flaky.json is absolute, using as is
2026-04-29 05:54:38.999 | DEBUG    | otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:38.999 | W:73742  | DEBUG    | copy flaky demo::otter.storage.synchronous.handle:_resolve:84 - location input/retry_demo/flaky.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/input/retry_demo/flaky.json
2026-04-29 05:54:39.000 | W:73742  | TRACE    | copy flaky demo::otter.validators.file:size:156 - size of http://127.0.0.1:8000/flaky.json: 28, size of input/retry_demo/flaky.json: 28
2026-04-29 05:54:39.000 | SUCCESS  | otter.step.worker:execute_task:107 - task=copy flaky demo phase=validate attempt=1/3 event=success
2026-04-29 05:54:39.000 | W:73742  | SUCCESS  | copy flaky demo::otter.step.worker:execute_task:107 - task=copy flaky demo phase=validate attempt=1/3 event=success
2026-04-29 05:54:39.001 | INFO     | otter.step.worker:run:75 - worker 0 completed task copy flaky demo
2026-04-29 05:54:39.001 | W:73742  | INFO     | otter.step.worker:run:75 - worker 0 completed task copy flaky demo
2026-04-29 05:54:39.981 | M:73739  | INFO     | otter.step.coordinator:_stop_workers:236 - stopping worker processes
2026-04-29 05:54:40.012 | INFO     | otter.step.worker:run:78 - worker 0 shutting down
2026-04-29 05:54:40.012 | W:73742  | INFO     | otter.step.worker:run:78 - worker 0 shutting down
2026-04-29 05:54:40.376 | INFO     | otter.step.worker:run:78 - worker 1 shutting down
2026-04-29 05:54:40.376 | W:73743  | INFO     | otter.step.worker:run:78 - worker 1 shutting down
2026-04-29 05:54:40.525 | M:73739  | SUCCESS  | otter.step.model:finish:42 - step retry_demo completed: took 5.088s
2026-04-29 05:54:40.525 | M:73739  | DEBUG    | otter.storage.synchronous.handle:_resolve:84 - location manifest.json resolved to local /Users/apple/Desktop/Projects/opensource/pipeline_work/manifest.json
2026-04-29 05:54:40.526 | M:73739  | INFO     | otter.storage.synchronous.filesystem:_read:74 - downloaded /Users/apple/Desktop/Projects/opensource/pipeline_work/manifest.json
2026-04-29 05:54:40.528 | M:73739  | INFO     | otter.manifest.model:_recalculate_result:158 - some steps in the manifest are still pending
2026-04-29 05:54:40.530 | M:73739  | SUCCESS  | otter.manifest.model:update:212 - step retry_demo updated successfully
```

- **What this output represents in terms of retry**

    This output demonstrates the main behavior of the prototype:

        1. retry applies to the task phase, not the whole step
        2. only retryable failures are retried
        3. backoff increases between attempts
        4. validation still runs after recovery
        5. the step no longer aborts on the first transient error





### Manifest 
(Example: check the [manifest.json](../pipeline_work/manifest.json`))

- The manifest also records the retry history for the task. In `pis_retry_demo.tasks[0].attempts`, the task shows:

        1. failed run attempt 1 with retryable: true
        2. failed run attempt 2 with retryable: true
        3. successful run attempt 3
        4. successful validate attempt 1

        The step itself is marked as success.

- This is the proof that retry history is not only visible in the terminal logs, but also preserved as execution provenance. That means this prototype does not just retry silently. It also records:

        1. which phase failed
        2. how many times it failed
        3. whether the failure was retryable
        4. how long Otter waited before retrying
        5. the final successful outcome

## Summary

This demo shows a working prototype of retry-with-backoff support in Otter.

In the original Otter behavior, a task failure stops the pipeline and is logged in the manifest. In this prototype, retryable failures are retried at the worker level before the task is marked as failed. The command-line logs show the backoff behavior, and the manifest shows the retry history and final success state.
