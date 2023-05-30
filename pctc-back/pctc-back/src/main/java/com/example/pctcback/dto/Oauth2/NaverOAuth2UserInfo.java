package com.example.pctcback.dto.Oauth2;

import java.util.Map;

public class NaverOAuth2UserInfo extends OAuth2UserInfo{
    public NaverOAuth2UserInfo(Map<String, Object> attributes) {
        super(attributes);
    }
    Map<String,Object> parser = (Map<String, Object>) attributes.get("response");

    @Override
    public String getId() {
        String response = (String) parser.get("id");
        return response;
    }

    @Override
    public String getNickname() {
        String Nickname = (String) parser.get("name");
        return Nickname;
    }

    @Override
    public String getEmail() {
        String Email = (String) parser.get("email");
        return Email;
    }
}
