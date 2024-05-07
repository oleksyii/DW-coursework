import axios from "axios";
import { AUTH_TOKEN_KEY } from "@/utils/constants";

const headers = {
  Accept: "application/json",
  "Content-Type": "application/json; charset=utf-8",
  "X-Requested-With": "XMLHttpRequest",
  // 'Access-Control-Allow-Credentials': true,
};

class HttpClient {
  #instance = null;

  get httpClient() {
    return this.#instance !== null ? this.#instance : this.initHttpClient();
  }

  initHttpClient() {
    const http = axios.create({
      baseURL: import.meta.env.VITE_BASE_API,
      headers,
      // withCredentials: true,
    });
    http.interceptors.request.use(injectToken, (error) =>
      Promise.reject(error)
    );

    http.interceptors.response.use(
      (response) => response,
      (error) => {
        return this.#handleError(error);
      }
    );
    this.#instance = http;
    return http;
  }

  #handleError(error) {
    const errorData = {
      code: error.status,
      message: error?.response?.data?.message
        ? error?.response?.data?.message
        : error.message,
      status: error.statusText,
    };
    console.log(error);
    return Promise.reject(errorData);
  }

  request(config) {
    return this.httpClient.request(config);
  }

  get(url, config) {
    return this.httpClient.get(url, config);
  }

  post(url, data, config) {
    return this.httpClient.post(url, data, config);
  }

  put(url, data, config) {
    return this.httpClient.put(url, data, config);
  }

  delete(url, config) {
    return this.httpClient.delete(url, config);
  }
}

export const httpClient = new HttpClient();
