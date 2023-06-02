package com.example.pctcback.security;

import com.example.pctcback.Role;
import lombok.Getter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;

import java.util.Collection;
import java.util.Map;
@Getter
public class CustomOath2User extends DefaultOAuth2User {
    private final String nickname;

    private final String email;

    private final Role role;

    private final String token;


    /**
     * Constructs a {@code DefaultOAuth2User} using the provided parameters.
     *
     * @param authorities      the authorities granted to the user
     * @param attributes       the attributes about the user
     * @param nameAttributeKey the key used to access the user's &quot;name&quot; from
     *                         {@link #getAttributes()}
     */
    public CustomOath2User(Collection<? extends GrantedAuthority> authorities, Map<String, Object> attributes, String nameAttributeKey, String email, Role role, String token , String nickname) {
        super(authorities, attributes, nameAttributeKey);
        this.email = email;
        this.role = role;
        this.token = token;
        this.nickname = nickname;
    }
}
