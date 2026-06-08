from flows.flow import main_flow


if __name__ == "__main__":
    main_flow.serve(
        name="main-flow-stage",
        interval=300,
    )
