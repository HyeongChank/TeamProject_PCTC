package com.example.pctcback.security;
import com.example.pctcback.persistence.UserRepository;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationSuccessHandler;
import org.springframework.stereotype.Component;
import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

@Slf4j
@Component
public class OAuthSuccessHandler extends SimpleUrlAuthenticationSuccessHandler {
    TokenProvider tokenProvider;
    final
    UserRepository userRepo;

    public OAuthSuccessHandler(TokenProvider tokenProvider, UserRepository userRepo) {
        this.tokenProvider = tokenProvider;
        this.userRepo = userRepo;
    }

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException {
        // Get the custom user object from the authentication object
        CustomOath2User oath2User = (CustomOath2User) authentication.getPrincipal();
        if(authentication.getPrincipal().getClass() == CustomOath2User.class){
            //Create token using the custom user object
            String token = oath2User.getToken();
            String nickname = oath2User.getNickname();
            String encodedNickname = URLEncoder.encode(nickname, StandardCharsets.UTF_8);
            response.getWriter().write(token);
            log.info("Social Login Success. ");
            log.info("token {}", token);
            response.sendRedirect("http://10.125.121.207:3000/logined?"+token+"nickname?"+encodedNickname);
//            response.sendRedirect("http://localhost:3000/logined?"+token+"nickname?"+encodedNickname);
        }
    }
}
