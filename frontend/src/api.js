import axios from "axios";

const API = axios.create({
  baseURL: "https://hrms-repo-m3n3.onrender.com",
});

export default API;