import { log } from "console";
import api from "./api";

interface RegisterData {
  username: string;
  password: string;
}

export const register = ({ username, password }: RegisterData) => {
  console.log("register", username, password);
  console.log(process.env.NEXT_PUBLIC_SERVER_URL);

  return api.post("/auth/register", {
    username,
    password,
  });
};

export const login = ({ username, password }: RegisterData) => {
  return api.post("/auth/login", {
    username,
    password,
  });
};
