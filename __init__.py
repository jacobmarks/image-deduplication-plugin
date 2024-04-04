"""Image Deduplication plugin.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import os

import fiftyone as fo
from fiftyone.core.utils import add_sys_path
import fiftyone.operators as foo
from fiftyone.operators import types


def _execution_mode(ctx, inputs):
    delegate = ctx.params.get("delegate", False)

    if delegate:
        description = "Uncheck this box to execute the operation immediately"
    else:
        description = "Check this box to delegate execution of this task"

    inputs.bool(
        "delegate",
        default=False,
        required=True,
        label="Delegate execution?",
        description=description,
        view=types.CheckboxView(),
    )

    if delegate:
        inputs.view(
            "notice",
            types.Notice(
                label=(
                    "You've chosen delegated execution. Note that you must "
                    "have a delegated operation service running in order for "
                    "this task to be processed. See "
                    "https://docs.voxel51.com/plugins/index.html#operators "
                    "for more information"
                )
            ),
        )


def get_similarity_runs(dataset):
    """
    Returns a list of similarity runs for the given dataset.
    """

    similarity_runs = []
    for br in dataset.list_brain_runs():
        if "Similarity" in dataset.get_brain_info(br).config.cls:
            similarity_runs.append(br)

    return similarity_runs


class FindExactDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="find_exact_duplicate_images",
            label="Dedup: Find exact duplicates",
            description="Find exact duplicates in the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/exact_dup.svg"
        return _config

    def resolve_delegation(self, ctx):
        return ctx.params.get("delegate", False)

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Find exact duplicates",
            description="Find exact duplicates in the dataset",
        )
        _execution_mode(ctx, inputs)
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from exact_dups import find_exact_duplicates

        sample_collection = ctx.dataset

        response = find_exact_duplicates(sample_collection)
        ctx.ops.reload_dataset()
        return response

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str(
            "num_images_with_exact_dups",
            label="Number of images with exact duplicates",
        )
        outputs.str("num_dups", label="Number of exact duplicates")
        header = "Exact Duplicate Results"
        return types.Property(outputs, view=types.View(label=header))


class DisplayExactDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="display_exact_duplicate_groups",
            label="Dedup: Display exact duplicates",
            description="Display exact duplicates in the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/view_groups.svg"
        return _config

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Display exact duplicates",
            description="Display exact duplicates in the dataset",
        )
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from exact_dups import get_exact_duplicate_groups

        view = get_exact_duplicate_groups(ctx.dataset)
        ctx.ops.set_view(view=view)


class RemoveAllExactDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="remove_all_exact_duplicates",
            label="Dedup: Remove all exact duplicates",
            description="Remove all exact duplicates from the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/delete.svg"
        return _config

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Remove all exact duplicates",
            description="Remove all exact duplicates from the dataset",
        )
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from exact_dups import remove_all_exact_duplicates

        remove_all_exact_duplicates(ctx.dataset)
        ctx.ops.reload_dataset()


class DeduplicateExactDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="deduplicate_exact_duplicates",
            label="Dedup: Deduplicate exact duplicates",
            description="Remove all but one copy from each group of exact duplicates in the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/representative.svg"
        return _config

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Deduplicate exact duplicates",
            description="Deduplicate exact duplicates in the dataset",
        )
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from exact_dups import deduplicate_exact_duplicates

        deduplicate_exact_duplicates(ctx.dataset)
        ctx.ops.reload_dataset()


class FindApproximateDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="find_approximate_duplicate_images",
            label="Dedup: Find approximate duplicates",
            description="Find approximate duplicates in the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/approx_dup.svg"
        return _config

    def resolve_delegation(self, ctx):
        return ctx.params.get("delegate", False)

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Find Approximate Duplicates",
            description="Find approximate duplicates in the dataset using embeddings",
        )

        sim_keys = get_similarity_runs(ctx.dataset)
        if len(sim_keys) == 0:
            inputs.str(
                "no_similarity_run_warning",
                view=types.Warning(
                    label=f"No Similarity Runs",
                    description="You must generate a similarity index on the dataset before you can find approximate duplicates. \n\nSee ```fob.compute_similarity()```",
                ),
            )
        else:
            sim_choices = types.Dropdown(label="Similarity Run")
            for sim_key in sim_keys:
                sim_choices.add_choice(sim_key, label=sim_key)
            inputs.enum(
                "sim_choices",
                sim_choices.values(),
                default=sim_choices.choices[0].value,
                view=sim_choices,
            )

            method_choices = types.RadioGroup()
            method_choices.add_choice("threshold", label="Threshold")
            method_choices.add_choice("fraction", label="Fraction")
            inputs.enum(
                "method_choices",
                method_choices.values(),
                default=method_choices.choices[0].value,
                label="Approximate Duplicate Selection Method",
                view=method_choices,
            )

            if ctx.params.get("method_choices", False) == "fraction":
                fraction_slider = types.SliderView(
                    label="Fraction of dataset to select",
                    description="Select the fraction of the dataset to mark as approximate duplicates",
                    componentsProps={
                        "slider": {"min": 0, "max": 1, "step": 0.01}
                    },
                )
                inputs.float("dup_fraction", default=0.1, view=fraction_slider)
            else:
                inputs.float(
                    "threshold_value",
                    default=0.5,
                    label="Distance Threshold",
                    description="Select the distance threshold for determining approximate duplicates",
                )

        _execution_mode(ctx, inputs)
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from approx_dups import find_approximate_duplicates

        sample_collection = ctx.dataset
        method = ctx.params.get("method", "None provided")
        brain_key = ctx.params.get("sim_choices", None)

        if method == "fraction":
            fraction = ctx.params.get("dup_fraction", 0.1)
            response = find_approximate_duplicates(
                sample_collection, brain_key, fraction=fraction
            )
        else:
            threshold = ctx.params.get("threshold_value", 0.5)
            response = find_approximate_duplicates(
                sample_collection, brain_key, threshold=threshold
            )

        return response

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str(
            "num_images_with_approx_dups",
            label="Number of images with approximate duplicates",
        )
        outputs.str("num_dups", label="Number of approximate duplicates")
        header = "Approximate Duplicate Results"
        return types.Property(outputs, view=types.View(label=header))


class DisplayApproximateDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="display_approximate_duplicate_groups",
            label="Dedup: Display approximate duplicates",
            description="Display approximate duplicates in the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/view_groups.svg"
        return _config

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Display approximate duplicates",
            description="Display approximate duplicates in the dataset",
        )
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from approx_dups import get_approximate_duplicate_groups

            view = get_approximate_duplicate_groups(ctx.dataset)
            ctx.ops.set_view(view=view)


class RemoveAllApproximateDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="remove_all_approximate_duplicates",
            label="Dedup: Remove all approximate duplicates",
            description="Remove all approximate duplicates from the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/delete.svg"
        return _config

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Remove all approximate duplicates",
            description="Remove all approximate duplicates from the dataset",
        )
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from approx_dups import remove_all_approximate_duplicates

        remove_all_approximate_duplicates(ctx.dataset)
        ctx.ops.reload_dataset()


class DeduplicateApproximateDuplicates(foo.Operator):
    @property
    def config(self):
        _config = foo.OperatorConfig(
            name="deduplicate_approximate_duplicates",
            label="Dedup: Deduplicate approximate duplicates",
            description="Remove all but one copy from each group of approximate duplicates in the dataset",
            dynamic=True,
        )
        _config.icon = "/assets/representative.svg"
        return _config

    def resolve_input(self, ctx):
        inputs = types.Object()
        form_view = types.View(
            label="Deduplicate approximate duplicates",
            description="Deduplicate approximate duplicates in the dataset",
        )
        return types.Property(inputs, view=form_view)

    def execute(self, ctx):
        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=no-name-in-module,import-error
            from approx_dups import deduplicate_approximate_duplicates

        deduplicate_approximate_duplicates(ctx.dataset)
        ctx.ops.reload_dataset()


def register(plugin):
    plugin.register(FindExactDuplicates)
    plugin.register(DisplayExactDuplicates)
    plugin.register(RemoveAllExactDuplicates)
    plugin.register(DeduplicateExactDuplicates)
    plugin.register(FindApproximateDuplicates)
    plugin.register(DisplayApproximateDuplicates)
    plugin.register(RemoveAllApproximateDuplicates)
    plugin.register(DeduplicateApproximateDuplicates)
