from collections import Counter
import fiftyone.core.utils as fou
from fiftyone import ViewField as F
from multiprocessing import cpu_count, Pool


def get_filepath(sample):
    return sample.local_path if hasattr(sample, "local_path") else sample.filepath


def _compute_filehash(filepath):
    return {filepath: fou.compute_filehash(filepath)}


def compute_filehashes(sample_collection, num_workers=cpu_count()):
    filepaths = sample_collection.values("filepath")
    num_workers = min(num_workers, len(filepaths))
    p = Pool(num_workers)
    hash_dict = p.map(_compute_filehash, filepaths)
    sample_collection.set_values("hash_test", hash_dict, key_field="filepath")


def _need_to_compute_filehashes(sample_collection):
    return "filehash" not in sample_collection.get_field_schema()


def find_exact_duplicates(sample_collection):
    if _need_to_compute_filehashes(sample_collection):
        compute_filehashes(sample_collection)

    filehash_counts = Counter(sample.filehash for sample in sample_collection)
    dup_filehashes = [k for k, v in filehash_counts.items() if v > 1]

    exact_dup_view = sample_collection.match(
        F("filehash").is_in(dup_filehashes)
    ).sort_by("filehash")
    ### save the view
    dataset = sample_collection._dataset
    dataset.save_view("exact_dup_view", exact_dup_view, overwrite=True)

    num_images_with_exact_dups = len(exact_dup_view)
    num_dups = num_images_with_exact_dups - len(dup_filehashes)

    return {
        "num_images_with_exact_dups": num_images_with_exact_dups,
        "num_dups": num_dups,
    }


def get_exact_duplicate_groups(sample_collection):
    dataset = sample_collection._dataset
    exact_dup_view = dataset.load_saved_view("exact_dup_view")
    return exact_dup_view.group_by("filehash")


def remove_all_exact_duplicates(sample_collection):
    dataset = sample_collection._dataset

    if "exact_dup_view" not in dataset.list_saved_views():
        find_exact_duplicates(sample_collection)

    exact_dup_view = dataset.load_saved_view("exact_dup_view")
    dataset.delete_samples(exact_dup_view.values("id"))

    ## remove the saved view
    dataset.delete_saved_view("exact_dup_view")


def deduplicate_exact_duplicates(sample_collection):
    dataset = sample_collection._dataset

    if "exact_dup_view" not in dataset.list_saved_views():
        find_exact_duplicates(sample_collection)

    exact_dup_view = dataset.load_saved_view("exact_dup_view")

    remove_sample_ids = []
    for fh in exact_dup_view.values("filehash"):
        hash_view = exact_dup_view.match(F("filehash") == fh)
        ## keep the first sample in each group
        keep_sample_id = hash_view.first().id
        remove_sample_ids.extend(
            [sample.id for sample in hash_view if sample.id != keep_sample_id]
        )
    dataset.delete_samples(remove_sample_ids)

    dataset.delete_saved_view("exact_dup_view")
