import argparse

from manager import ManagerAgent


def demo_basic():
    manager = ManagerAgent()
    goal = "Explain binary search algorithm with a simple example"
    result = manager.execute_goal(goal)
    print("\n" + "="*60)
    print("FINAL OUTPUT")
    print("="*60)
    print(result["final_output"])
    return result


def demo_coding():
    manager = ManagerAgent()
    goal = "Implement a function to find the maximum element in a list"
    result = manager.execute_goal(goal)
    print("\n" + "="*60)
    print("FINAL OUTPUT")
    print("="*60)
    print(result["final_output"])
    return result


def demo_custom(custom_goal: str):
    manager = ManagerAgent()
    result = manager.execute_goal(custom_goal)
    print("\n" + "="*60)
    print("FINAL OUTPUT")
    print("="*60)
    print(result["final_output"])
    return result


def main():
    parser = argparse.ArgumentParser(description="Run ManagerAgent demos")
    parser.add_argument("--goal", type=str, help="Custom goal to run", default=None)
    args = parser.parse_args()

    if args.goal:
        demo_custom(args.goal)
    else:
        demo_basic()


if __name__ == "__main__":
    main()
