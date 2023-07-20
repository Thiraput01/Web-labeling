import { atom } from "jotai";

export interface DataItem {
  id: string;
  title: string;
  url: string;
  coordinateX: number;
  coordinateY: number;
  type: string;
  dataSetId: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserData {
  id: string;
  userId: string;
  dataId: string;
  isLabelled: boolean;
  answer: string;
}

export const dataAtom = atom<DataItem | undefined>(undefined);
