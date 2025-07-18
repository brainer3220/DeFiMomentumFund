from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from defi_fund.state import load_state

app = FastAPI(title="DeFi Fund Admin")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
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
