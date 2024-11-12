import unreal
from enum import StrEnum

class Prefix(StrEnum):
    TEXTURE2D = "T_"
    MATERIAL = "M_"
    MATERIAL_INSTANCE_CONSTANT = "MI_"
    BLUEPRINT = "BP_"

@unreal.uclass()
class SetPrefix(unreal.ToolMenuEntryScript):
    EditorAssetLib = unreal.EditorAssetLibrary()

    PREFIX_MAPPING = {
        unreal.Texture2D: Prefix.TEXTURE2D,
        unreal.Material: Prefix.MATERIAL,
        unreal.MaterialInstanceConstant: Prefix.MATERIAL_INSTANCE_CONSTANT,
        unreal.Blueprint: Prefix.BLUEPRINT,
    }
    EXISTING_PREFIXES = {
        Prefix.TEXTURE2D,
        Prefix.MATERIAL,
        Prefix.MATERIAL_INSTANCE_CONSTANT,
        Prefix.BLUEPRINT,
        "Blueprint",
        "blueprint",
        "PPM_",
        "PPMI_",
    }

    EXCLUSIONS = {
        "MM_"
    }
    
    SUFFIXES = {
        "_Inst"
    }

    def remove_suffix_from_asset(self, asset_name: str):
        for suffix in self.SUFFIXES:
            if asset_name.endswith(suffix):
                asset_name = asset_name[: -len(suffix)]
                return

    def fix_prefix(self, directory: str, apply_fix: bool = True):
        asset_path_list = self.EditorAssetLib.list_assets(directory, recursive=True)
        steps = len(asset_path_list)

        with unreal.ScopedSlowTask(steps, "Fixing prefixes for assets...") as slow_task:
            slow_task.make_dialog_delayed(1.5, can_cancel=True)

            for asset_path in asset_path_list:
                if slow_task.should_cancel():
                    unreal.log("Task was canceled by the user.")
                    break

                asset = self.EditorAssetLib.load_asset(asset_path)
                asset_name = asset.get_name()

                if any(
                    asset_name.startswith(exclusion) for exclusion in self.EXCLUSIONS
                ):
                    print(f"Skipping {asset_name} due to exclusion prefix.")
                    slow_task.enter_progress_frame(1)
                    continue

                correct_prefix = None
                for asset_type, prefix in self.PREFIX_MAPPING.items():
                    if isinstance(asset, asset_type):
                        correct_prefix = prefix

                        for existing_prefix in self.EXISTING_PREFIXES:
                            if asset_name.startswith(existing_prefix):
                                asset_name = asset_name[len(existing_prefix) :]
                                break

                        if isinstance(asset, unreal.Material):
                            material_domain = asset.get_editor_property(
                                "material_domain"
                            )
                            is_postprocess = (
                                material_domain == unreal.MaterialDomain.MD_POST_PROCESS
                            )

                            if is_postprocess:
                                ppm_directory = "/Game/PostProcessMaterials"
                                if not self.EditorAssetLib.does_directory_exist(
                                    ppm_directory
                                ):
                                    self.EditorAssetLib.make_directory(ppm_directory)

                                self.remove_suffix_from_asset(asset_name)

                                new_name = "PPM_" + asset_name
                                new_path = f"{ppm_directory}/{new_name}"

                                if apply_fix:
                                    success = self.EditorAssetLib.rename_asset(
                                        asset_path, new_path
                                    )
                                    if success:
                                        print(
                                            f"Renamed {asset_name} to {new_name} in PostProcessMaterials directory."
                                        )
                                    else:
                                        print(f"Failed to rename {asset_name}")
                                else:
                                    print(
                                        f"Suggested rename for post-process material: {asset_name} to {new_name}"
                                    )

                                slow_task.enter_progress_frame(1)
                                continue

                        self.remove_suffix_from_asset(asset_name)

                        new_name = correct_prefix + asset_name
                        new_path = "/".join(asset_path.split("/")[:-1]) + "/" + new_name

                        if apply_fix:
                            success = self.EditorAssetLib.rename_asset(
                                asset_path, new_path
                            )
                            if success:
                                print(f"Renamed {asset.get_name()} to {new_name}")
                            else:
                                print(f"Failed to rename {asset_name}")
                        else:
                            print(f"Suggested rename: {asset_name} to {new_name}")
                        break
                slow_task.enter_progress_frame(1)

    # override execute to call fix_prefix
    @unreal.ufunction(override=True)
    def execute(self, context):  # type: ignore
        # calls fix_prefix when menu item is selected
        self.fix_prefix("/Game", apply_fix=True)
