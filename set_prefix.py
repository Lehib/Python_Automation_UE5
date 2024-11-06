import unreal

# TASK ONE: GET THIS VERSIONED ON GITHUB in case this becomes too heavy and it's better to go back

# next steps: adding GUI to give users option of adding or removing EXISTING_PREFIXES and EXCLUSIONS
# adding a variable for the directory name to + to ppm_directory = "Game/Content/" and allow users to alter the directory
# only do the above line if there are other special items that might want a new directory of their own
# gather a larger list for PREFIX_MAPPING, and maybe see if it's possible to give users access to change the values
# I want the ppm directory to find a materials directory and be made there if one exists and if a PostProcessMaterials folder
# exists elsewhere already outside of materials folder then delete it, otherwise, do the thing it's doing currently


# Initialize the Editor Asset Library
EditorAssetLib = unreal.EditorAssetLibrary()

# Define prefix mapping for asset types
PREFIX_MAPPING = {
    unreal.Texture2D: "T_",
    unreal.Material: "M_",
    unreal.MaterialInstanceConstant: "MI_",
    unreal.Blueprint: "BP_"
}

# Define a set of all existing prefixes to strip from asset names
EXISTING_PREFIXES = {"T_", "M_", "MI_", "BP_", "Blueprint", "blueprint", "PPM_"}

# Define a set of prefixes to exclude from renaming
EXCLUSIONS = {"MM_"}

SUFFIXES = {"_Inst"}

def fix_prefix(directory: str, apply_fix: bool = True):
    asset_path_list = EditorAssetLib.list_assets(directory, recursive=True)
    steps = len(asset_path_list)  # Set steps based on the number of assets

    # Start the progress task
    with unreal.ScopedSlowTask(steps, "Fixing prefixes for assets...") as slow_task:
        slow_task.make_dialog_delayed(1.5, can_cancel=True)  # Show dialog after 1.5s delay

        for asset_path in asset_path_list:
            if slow_task.should_cancel():  # Allow cancellation
                unreal.log("Task was canceled by the user.")
                break

            asset = EditorAssetLib.load_asset(asset_path)
            asset_name = asset.get_name()

            # Skip assets with any exclusion prefix
            if any(asset_name.startswith(exclusion) for exclusion in EXCLUSIONS):
                print(f"Skipping {asset_name} due to exclusion prefix.")
                slow_task.enter_progress_frame(1)  # Update progress even if skipped
                continue

            correct_prefix = None
            for asset_type, prefix in PREFIX_MAPPING.items():
                if isinstance(asset, asset_type):
                    correct_prefix = prefix

                    # Remove any existing prefix from the list
                    for existing_prefix in EXISTING_PREFIXES:
                        if asset_name.startswith(existing_prefix):
                            asset_name = asset_name[len(existing_prefix):]  # Strip existing prefix
                            break

                    # Handle post-process materials separately
                    if isinstance(asset, unreal.Material):
                        material_domain = asset.get_editor_property("material_domain")
                        is_postprocess = material_domain == unreal.MaterialDomain.MD_POST_PROCESS

                        if is_postprocess:
                            ppm_directory = "/Game/PostProcessMaterials"
                            
                            if not EditorAssetLib.does_directory_exist(ppm_directory):
                                EditorAssetLib.make_directory(ppm_directory)

                            for suffixes in SUFFIXES:
                                if asset_name.endswith(suffixes):
                                    asset_name = asset_name[:-len(suffixes)]  # Strip unwanted suffix
                                    break
                            new_name = "PPM_" + asset_name
                            new_path = f"{ppm_directory}/{new_name}"

                            if apply_fix:
                                success = EditorAssetLib.rename_asset(asset_path, new_path)
                                if success:
                                    print(f"Renamed {asset_name} to {new_name} in PostProcessMaterials directory.")
                                else:
                                    print(f"Failed to rename {asset_name}")
                            else:
                                print(f"Suggested rename for post-process material: {asset_name} to {new_name}")

                            # Skip further processing for post-process materials
                            slow_task.enter_progress_frame(1)  # Update progress
                            continue

                    # For non-post-process assets, apply the correct prefix
                    for suffixes in SUFFIXES:
                        if asset_name.endswith(suffixes):
                            asset_name = asset_name[:-len(suffixes)]  # Strip unwanted suffix
                            break
                    new_name = correct_prefix + asset_name
                    new_path = "/".join(asset_path.split("/")[:-1]) + "/" + new_name

                    if apply_fix:
                        success = EditorAssetLib.rename_asset(asset_path, new_path)
                        if success:
                            print(f"Renamed {asset.get_name()} to {new_name}")
                        else:
                            print(f"Failed to rename {asset_name}")
                    else:
                        print(f"Suggested rename: {asset_name} to {new_name}")

                    # Exit the `PREFIX_MAPPING` loop after applying the correct prefix
                    break

            # Update the progress for each asset processed
            slow_task.enter_progress_frame(1)

if __name__ == "__main__":
    fix_prefix("/Game", True)
