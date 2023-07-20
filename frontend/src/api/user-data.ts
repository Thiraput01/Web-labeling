import api from "./api";

export const markAsLabelled = (
  answer: string,
  userId: string,
  dataId: string
) => {
  return api.post(`/user-data/mark-as-labelled`, {
    answer,
    userId,
    dataId,
  });
};

export const changeAnswer = (
  answer: string,
  userId: string,
  dataId: string
) => {
  return api.post(`/user-data/update-answer`, { answer, userId, dataId });
};

export const getUserDataByUserIdAndDataId = (
  userId: string,
  dataId: string
) => {
  return api.post(`/user-data/user/data`, { userId, dataId });
};
