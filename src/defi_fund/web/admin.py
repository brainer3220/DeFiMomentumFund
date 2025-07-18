"""Simple admin dashboard with basic auth."""

import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from defi_fund.state import load_state

security = HTTPBasic()


def verify(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """Validate provided credentials against environment variables."""
    user = os.getenv("ADMIN_USER", "admin")
    password = os.getenv("ADMIN_PASS")
    if not password:
        raise RuntimeError("ADMIN_PASS env var not set")

    user_ok = secrets.compare_digest(credentials.username, user)
    pass_ok = secrets.compare_digest(credentials.password, password)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )

app = FastAPI(title="DeFi Fund Admin")


@app.get("/", response_class=HTMLResponse)
def index(_: None = Depends(verify)) -> HTMLResponse:
    state = load_state()
    html = f"""
    <html>
        <head><title>DeFi Fund Admin</title></head>
        <body>
            <h1>Fund State</h1>
            <ul>
                <li>Total Assets: {state['total_assets']:.4f}</li>
                <li>Total Shares: {state['total_shares']:.4f}</li>
                <li>Mgmt Acc: {state['mgmt_acc']:.4f}</li>
                <li>Perf Acc: {state['perf_acc']:.4f}</li>
                <li>HWM: {state['hwm']:.4f}</li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


def main() -> None:
    import uvicorn

    uvicorn.run("defi_fund.web.admin:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
