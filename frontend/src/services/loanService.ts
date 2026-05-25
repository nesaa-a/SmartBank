import { api } from "./api";
import type { LoanApplicationRequest, LoanPredictionResult } from "../types/loan";

export const loanService = {
  async predict(data: LoanApplicationRequest): Promise<LoanPredictionResult> {
    const res = await api.post<LoanPredictionResult>("/loan/predict", data);
    return res.data;
  },
};
