import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import Signup from "./Signup.tsx";
import { RecoilRoot } from "recoil";
import "./index.css";
import { ChainlitAPI, ChainlitContext } from "@chainlit/react-client";
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const CHAINLIT_SERVER = "http://localhost:80/chainlit";

const apiClient = new ChainlitAPI(CHAINLIT_SERVER, "webapp");

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <RecoilRoot>
        <Signup />
      </RecoilRoot>
    ),
  },
  {
    path: '/chat',
    element: (
      <RecoilRoot>
        <App />
      </RecoilRoot>
    ),
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ChainlitContext.Provider value={apiClient}>
      <RouterProvider router={router} />
    </ChainlitContext.Provider>
  </React.StrictMode>
);