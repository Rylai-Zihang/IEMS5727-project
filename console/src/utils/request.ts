import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";

interface InterceptorFunction {
  (config: AxiosRequestConfig): AxiosRequestConfig;
  (error: any): Promise<any>;
}

const service: AxiosInstance = axios.create({
  baseURL: "/",
  timeout: 5000,
});

// 请求拦截器
service.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use((response: AxiosResponse) => {
  const { status, message, data } = response.data;
  if (status) {
    return data;
  } else {
    return Promise.reject(new Error(message));
  }
});

export default service;
