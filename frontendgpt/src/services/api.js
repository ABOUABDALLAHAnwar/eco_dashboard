import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8001",
});

export const getAllActions = async () => {
  const response = await api.get("/all_actions_templates");
  return response.data;
};
