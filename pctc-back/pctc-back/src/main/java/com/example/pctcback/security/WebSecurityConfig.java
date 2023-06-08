package com.example.pctcback.security;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@EnableWebSecurity(debug = true)
    @Configuration
    @Slf4j
    public class WebSecurityConfig /*implements WebMvcConfigurer */{
        @Autowired
        private CustomOAth2UserService customOAuth2UserService;
        @Autowired
        private OAuthSuccessHandler oAuthSuccessHandler;
        @Bean
        protected SecurityFilterChain configure(HttpSecurity http)throws Exception{
            http.cors() // WebMvCConfig 에서 설정이 이루어졌으므로.
                    .and()
                    .csrf().disable()
                    .formLogin().disable()
                    .sessionManagement()
                    .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                    .and()
                    .authorizeHttpRequests(authorize -> authorize
                            .requestMatchers("/**","/port","/auth/**","/oauth2/**","/user/**","/favicon.ico").permitAll()
                            .shouldFilterAllDispatcherTypes(false)
                            .anyRequest()
                            .authenticated())
                    .oauth2Login()
                    .userInfoEndpoint()
                    .userService(customOAuth2UserService)
                    .and().successHandler(oAuthSuccessHandler);

            //filter 등록.
            //매 요청마다 Corsfilter 실행한 후에
            //jwtAuthenticationFilter 실행한다.
            return http.build();
        }
    }
