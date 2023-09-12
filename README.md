## Image Deduplication Plugin

This plugin is a Python plugin that streamlines image deduplication workflows!

With this plugin, you can:

- Find _exact_ duplicate images using a hash function
- Find _near_ duplicate images using an embedding model and similarity threshold
- View and interact with duplicate images in the App
- Remove all duplicates, or keep a representative image from each duplicate set

It demonstrates how to do the following:

- Set the session's view with a trigger and serialization
- Split your Python code into multiple files and import them into your plugin

## Installation

```shell
fiftyone plugins download https://github.com/jacobmarks/image-deduplication-plugin
```

## Operators

### `find_approximate_duplicate_images`

This operator finds near-duplicate images in a dataset using a specified similarity index paired with either a distance threshold or a fraction of samples to mark as duplicates.

### `find_exact_duplicate_images`

![find_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/27c12f82-bd8f-45d7-9213-d5b9ceb99bcb)

This operator finds exact duplicate images in a dataset using a hash function.

### `display_approximate_duplicate_groups`

This operator displays the images in a dataset that are near-duplicates of each other, grouped together.

### `display_exact_duplicate_groups`
![display_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/19fec753-52d1-4237-9e24-78bc89a40af0)

This operator displays the images in a dataset that are exact duplicates of each other, grouped together.

### `remove_all_approximate_duplicates`

This operator removes all near-duplicate images from a dataset.

### `remove_all_exact_duplicates`
![remove_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/59b26da7-9064-4da0-8fa8-85488e99b57c)

This operator removes all exact duplicate images from a dataset.

### `deduplicate_approximate_duplicates`

This operator removes near-duplicate images from a dataset, _keeping a representative image_ from each duplicate set.

### `deduplicate_exact_duplicates`

![dedup_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/30abc333-0f60-4a7a-a461-1b9dd6eb8331)

This operator removes exact duplicate images from a dataset, _keeping a representative image_ from each duplicate set.
