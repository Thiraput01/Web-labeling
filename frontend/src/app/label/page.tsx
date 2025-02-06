"use client";
import React, { useEffect, useState } from "react";
import { Button, Card, Radio, Spin } from "antd";
import {
  changeAnswer,
  getUserDataByUserIdAndDataId,
  markAsLabelled,
} from "@/api/user-data";
import { useAtom } from "jotai";
import Navbar from "@/components/navbar";
import { UserData, dataAtom } from "@/atom/data-atom";
import { useRouter } from "next/navigation";
import { getMe } from "@/api/user";

const LabelPage: React.FC = () => {
  const router = useRouter();
  const [selectedLabel, setSelectedLabel] = useState("");
  const [userId, setUserId] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [data, setData] = useAtom(dataAtom);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userData, setUserData] = useState<UserData>({
    id: "",
    userId: "",
    dataId: "",
    isLabelled: false,
    answer: "",
  });

  if (typeof window !== "undefined") {
    if (!localStorage.getItem("isLogin")) {
      router.push("/login");
    }
  }

  if (!data) {
    router.push("/data");
  }

  useEffect(() => {
    fetchMe();
  }, []);

  const fetchMe = async () => {
    try {
      setIsLoading(true);
      const user = await getMe();
      setUsername(user.data.username);
      setUserId(user.data.id);
      const userData = await getUserDataByUserIdAndDataId(
        user.data.id,
        data ? data.id : ""
      );
      setUserData(userData.data);
      if (userData.data.isLabelled) {
        setSelectedLabel(userData.data.answer);
      }
      setIsLoading(false);
    } catch (error) {
      router.push("/data");
    }
  };

  const handleLabelSelection = (e: any) => {
    setSelectedLabel(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      if (data) {
        if (userData.isLabelled) {
          await changeAnswer(selectedLabel, userId, data.id);
        } else {
          await markAsLabelled(selectedLabel, userId, data.id);
        }
        router.push("/data");
      }
    } catch (error) {
      console.error("Failed to submit label:", error);
    }
  };

  return (
    <div>
      <Navbar username={username} />
      <Card className="flex justify-center items-center p-8 rounded-none">
        {isLoading ? (
          <Spin />
        ) : (
          <>
            <img
              src={data?.url}
              width={500}
              height={500}
              alt="Labelled Image"
            />
            <div className="mt-4">
              <Radio.Group
                onChange={handleLabelSelection}
                value={selectedLabel}
              >
                <Radio value="inside">Inside</Radio>
                <Radio value="near">Near</Radio>
                <Radio value="front">Front</Radio>
                <Radio value="far">Far</Radio>
                <Radio value="back">Back</Radio>
              </Radio.Group>
            </div>
            <div className="mt-4">
              <Button onClick={handleSubmit} disabled={!selectedLabel}>
                Submit
              </Button>
            </div>
          </>
        )}
      </Card>
    </div>
  );
};

export default LabelPage;
