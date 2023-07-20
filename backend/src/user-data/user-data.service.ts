import { Injectable } from '@nestjs/common';

import { UserData, Prisma } from '@prisma/client';

import { PrismaService } from 'src/libs/prisma/prisma.service';

@Injectable()
export class UserDataService {
  constructor(private readonly prisma: PrismaService) {}

  async getUserData(): Promise<UserData[]> {
    return this.prisma.userData.findMany();
  }

  async getUserDataById(id: string): Promise<UserData | null> {
    return this.prisma.userData.findUnique({ where: { id } });
  }

  async createUserData(
    data: Prisma.UserDataUncheckedCreateInput,
  ): Promise<UserData> {
    return this.prisma.userData.create({ data });
  }

  async updateUserData(
    id: string,
    data: Prisma.UserDataUncheckedUpdateInput,
  ): Promise<UserData> {
    return this.prisma.userData.update({ where: { id }, data });
  }

  async deleteUserData(id: string): Promise<UserData> {
    return this.prisma.userData.delete({ where: { id } });
  }

  async markAsLabelled(
    answer: string,
    userId: string,
    dataId: string,
  ): Promise<UserData> {
    const userData = await this.prisma.userData.findFirst({
      where: { userId, dataId },
    });
    if (userData?.isLabelled) {
      throw new Error('Data is already labelled');
    }

    return this.prisma.userData.update({
      where: { id: userData.id },
      data: { isLabelled: true, answer: answer },
    });
  }

  async updateAnswer(
    answer: string,
    userId: string,
    dataId: string,
  ): Promise<UserData> {
    const userData = await this.prisma.userData.findFirst({
      where: { userId, dataId },
    });
    if (!userData?.isLabelled) {
      throw new Error('Data is not labelled');
    }

    return this.prisma.userData.update({
      where: { id: userData.id },
      data: { answer: answer },
    });
  }

  async getUserDataByUserIdAndDataId(
    userId: string,
    dataId: string,
  ): Promise<UserData | null> {
    return this.prisma.userData.findFirst({ where: { userId, dataId } });
  }
}
