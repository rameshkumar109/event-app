import React from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Events from "./pages/Events";

function App() {
  const path = window.location.pathname || "/";
  const params = new URLSearchParams(window.location.search);
  const tokenFromQuery = params.get("token");
  const errorFromQuery = params.get("error");

  if (tokenFromQuery) {
    localStorage.setItem("gt_user_token", tokenFromQuery);
    window.history.replaceState({}, "", "/");
  }

  if (errorFromQuery) {
    window.history.replaceState({}, "", "/");
    return <Login errorOverride={errorFromQuery} />;
  }

  const token = localStorage.getItem("gt_user_token");

  if (path.startsWith("/register")) {
    return <Register />;
  }

  if (token) {
    return <Events />;
  }

  return <Login />;
}

export default App;
