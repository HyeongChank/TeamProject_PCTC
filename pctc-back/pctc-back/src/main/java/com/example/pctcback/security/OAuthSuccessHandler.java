package com.example.pctcback.security;

import com.example.pctcback.model.CustomOath2User;
import com.example.pctcback.persistence.UserRepository;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationSuccessHandler;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Slf4j
@Component
@AllArgsConstructor
public class OAuthSuccessHandler extends SimpleUrlAuthenticationSuccessHandler {
    @Autowired
    TokenProvider tokenProvider;
    @Autowired
    UserRepository userRepo;
    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException, ServletException {
        // Get the custom user object from the authentication object
        CustomOath2User oath2User = (CustomOath2User) authentication.getPrincipal();
        if(authentication.getPrincipal().getClass() == CustomOath2User.class){
            //Create token using the custom user object
            String token = oath2User.getToken();
            response.getWriter().write(token);
            log.info("Social Login Success. ");
            log.info("token {}", token);
            response.sendRedirect("http://localhost:8080/login?"+token);
        }
    }
}
