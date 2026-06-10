from core.config import settings
from flows.flow import main_flow

if __name__ == "__main__":
    main_flow.serve(
        name=settings().MAIN_DEPLOYMENT_NAME,
        interval=settings().MAIN_FLOW_INTERVAL_IN_SEC,
    )
