from Projects.Content_Factory.src.lip_sync.live_portrait_controller import LivePortraitController
import logging

logging.basicConfig(level=logging.INFO)


def run_test():
    controller = LivePortraitController()
    avatar = "Projects/Content_Factory/assets/avatars/unit_x.png"
    print(f"Testing LivePortrait with {avatar}...")
    try:
        result = controller.animate(avatar)
        if result:
            print(f"SUCCESS! Animation created at: {result}")
        else:
            print("FAILED: No output video generated.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")


if __name__ == "__main__":
    run_test()
