package com.example.pctcback.security;

import com.example.pctcback.AuthProvider;
import com.example.pctcback.model.User;
import com.example.pctcback.persistence.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserService;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.Map;


@Slf4j
@Service
@RequiredArgsConstructor
public class CustomOAth2UserService implements OAuth2UserService<OAuth2UserRequest,OAuth2User> {
    @Autowired
    private  UserRepository userRepo;
    @Autowired
    private TokenProvider tokenProvider;

    private static final String NAVER = "naver";
    private static final String KAKAO = "kakao";


    @Override
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        log.info("CustomOAuth2UserService is running ");
        OAuth2UserService<OAuth2UserRequest, OAuth2User> delegate = new DefaultOAuth2UserService();
        OAuth2User oAuth2User = delegate.loadUser(userRequest);


        String registrationId = userRequest.getClientRegistration().getRegistrationId();
        AuthProvider authProvider = getAuthProvider(registrationId);
        String userNameAttributeName = userRequest.getClientRegistration().getProviderDetails().getUserInfoEndpoint().getUserNameAttributeName();
        Map<String, Object> attributes = oAuth2User.getAttributes();
        OAuthAttributes extractAttributes = OAuthAttributes.of(authProvider, userNameAttributeName,attributes);
        User createdUser = getUser(extractAttributes, authProvider);
        String token = tokenProvider.create(createdUser);
        String nickname =createdUser.getNickname();

//         CustomOAuth2 USer 가져오기
        return  new CustomOath2User(
                Collections.singleton(new SimpleGrantedAuthority(createdUser.getRole().getKey())),
                attributes,
                extractAttributes.getNameAttributeKey(),
                createdUser.getEmail(),
                createdUser.getRole(),
                token,
                createdUser.getNickname()
                );

    }

    private AuthProvider getAuthProvider(String registrationId) {
        if (NAVER.equals(registrationId)) {
            return AuthProvider.NAVER;
        }

        if (KAKAO.equals(registrationId)) {
            return AuthProvider.KAKAO;
        }
        return AuthProvider.GOOGLE;
    }

    private User getUser(OAuthAttributes attributes, AuthProvider authProvider){
        User findUser = userRepo.findByUsername(authProvider.toString()+"_"+attributes.getOauth2UserInfo().getId());

        if(findUser == null){
            User createdUser = attributes.toEntity(authProvider, attributes.getOauth2UserInfo());

            return userRepo.save(createdUser);
        }
        return findUser;
    }

}
