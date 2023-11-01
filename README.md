## Image Deduplication Plugin

This plugin is a Python plugin that streamlines image deduplication workflows!

With this plugin, you can:

- Find _exact_ duplicate images using a hash function
- Find _near_ duplicate images using an embedding model and similarity threshold
- View and interact with duplicate images in the App
- Remove all duplicates, or keep a representative image from each duplicate set

## Watch On Youtube
[![Video Thumbnail](https://img.youtube.com/vi/aingeh0KdPw/0.jpg)](https://www.youtube.com/watch?v=aingeh0KdPw&list=PLuREAXoPgT0RZrUaT0UpX_HzwKkoB-S9j&index=5)


## Installation

```shell
fiftyone plugins download https://github.com/jacobmarks/image-deduplication-plugin
```

## Operators

### `find_approximate_duplicate_images`
![find_approx_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/8cf44a01-505d-4942-8a24-2c2d65365894)


This operator finds near-duplicate images in a dataset using a specified similarity index paired with either a distance threshold or a fraction of samples to mark as duplicates.

### `find_exact_duplicate_images`

![find_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/27c12f82-bd8f-45d7-9213-d5b9ceb99bcb)

This operator finds exact duplicate images in a dataset using a hash function.

### `display_approximate_duplicate_groups`
![display_approx_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/07fefbd4-9df7-4ff5-8433-091629c2a040)

This operator displays the images in a dataset that are near-duplicates of each other, grouped together.

### `display_exact_duplicate_groups`
![display_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/19fec753-52d1-4237-9e24-78bc89a40af0)

This operator displays the images in a dataset that are exact duplicates of each other, grouped together.

### `remove_all_approximate_duplicates`
![remove_approx_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/1a23d1c1-3441-4286-b308-be99fb5f0a4a)

This operator removes all near-duplicate images from a dataset.

### `remove_all_exact_duplicates`
![remove_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/59b26da7-9064-4da0-8fa8-85488e99b57c)

This operator removes all exact duplicate images from a dataset.

### `deduplicate_approximate_duplicates`

![dedup_approx_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/f5661c6c-ebe9-41c6-9de8-a2c8048176f8)

This operator removes near-duplicate images from a dataset, _keeping a representative image_ from each duplicate set.

### `deduplicate_exact_duplicates`

![dedup_exact_dups](https://github.com/jacobmarks/image-deduplication-plugin/assets/12500356/30abc333-0f60-4a7a-a461-1b9dd6eb8331)

This operator removes exact duplicate images from a dataset, _keeping a representative image_ from each duplicate set.
