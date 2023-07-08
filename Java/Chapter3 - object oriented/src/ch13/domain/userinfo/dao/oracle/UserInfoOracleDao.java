package ch13.domain.userinfo.dao.oracle;

import ch13.domain.userinfo.UserInfo;
import ch13.domain.userinfo.dao.UserInfoDao;

public class UserInfoOracleDao implements UserInfoDao {
  @Override
  public void insertUserInfo(UserInfo userInfo) {
    System.out.println("Insert into Oracle DB userId = " + userInfo.getUserId());
  }

  @Override
  public void updateUserInfo(UserInfo userInfo) {
    System.out.println("Update into Oracle DB userId = " + userInfo.getUserId());
  }

  @Override
  public void deleteUserInfo(UserInfo userInfo) {
    System.out.println("Delete into Oracle DB userId = " + userInfo.getUserId());
  }
}
