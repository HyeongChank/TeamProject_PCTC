package com.example.pctcback.dto.Oauth2;

import lombok.extern.slf4j.Slf4j;

import java.util.Map;
@Slf4j
public class KaKaoOAuth2UserInfo extends OAuth2UserInfo{
    public KaKaoOAuth2UserInfo(Map<String, Object> attributes){
        super(attributes);
    }

    @Override
    public String getId() {
        return  attributes.get("id").toString();
    }

    @Override
    public String getNickname() {
        Map<String, Object> account = (Map<String, Object>) attributes.get("kakao_account");
        Map<String, Object> profile = (Map<String, Object>) account.get("profile");

        if(profile == null){
            log.info("Can't get a Account or Profile, check Configuration.");
            return  null;
        }
        return (String) profile.get("nickname");
    }

    @Override
    public String getEmail() {
        Map<String, Object> account = (Map<String, Object>) attributes.get("kakao_account");
        String email = (String) account.get("email");

        if(account == null){
            log.info("Can't get a Account or Profile, check Configuration.");
            return  null;
        }
        return email;}
    }

