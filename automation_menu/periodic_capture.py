import unreal

@unreal.uclass()
class PeriodicCapture(unreal.ToolMenuEntryScript):
    def CaptureViewport(self):
        # define the class of the actor you want to spawn
        camera_class = unreal.CameraActor.static_class()

        # define the location and rotation for the camera
        location = unreal.Vector(0.0, 0.0, 100.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)

        # spawn the camera actor
        camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(camera_class,location=location,rotation=rotation)

        # access camera actors viewport


        # Unreal function for taking a screen grab of that cameras viewport


        # find out if there’s a way to implement logic that takes those screen captures automatically upon file save

        # have an option for the user to change how many captures are taken based on whether it’s a longer or shorter sequence

        # give the script user the freedom to choose what the name is saved as and where

        # make the script automatically increment the saves name upon choosing a longer sequence if it doesn’t by default

        # maybe have the script save each sequence in its own numbered directory if it’s taking more than one snap so that  it doesn’t muddle up the versions, or if not have the increment feature also add a prefix that identifies them

        # it may be good to do it on autosave as an option too but if you want it to work best maybe it should be on playing the effect otherwise you won’t see anything, so whatever the button is to begin playing the effect should trigger the function, maybe with a buffer so that it won’t activate more than once a minute to avoid going overboard

    @unreal.ufunction(override=True)
    def execute(self, context): # type: ignore
        with unreal.ScopedEditorTransaction("Periodic Capture"):
            self.CaptureViewport()

# capture_script_object = PeriodicCapture()

# capture_script_object.init_entry(
#     owner_name=unreal.Name("PythonAutomation"),
#     menu=unreal.Name("LevelEditor.MainMenu.PythonAutomation"),
#     section=general_section_name,
#     name=unreal.Name("PeriodicCapture"),
#     label=unreal.Text("Periodic Capture"),
#     tool_tip=unreal.Text("Creates a camera for taking periodic screen captures")
# )

# capture_script_object.register_menu_entry()

# # icon
# capture_script_data = capture_script_object.data
# capture_script_icon = unreal.ScriptSlateIcon(
#     style_name=unreal.Name("Palette.Icon"),
#     small_style_name=unreal.Name("Palette.Icon.Small"),
#     style_set_name=unreal.Name("UMGStyle")
# )
# capture_script_data.icon = capture_script_icon

