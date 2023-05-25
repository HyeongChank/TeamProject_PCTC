package com.example.pctcback.security;

import com.example.pctcback.config.WebMvcConfig;
import lombok.extern.slf4j.Slf4j;
import org.apache.catalina.filters.CorsFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@EnableWebSecurity(debug = true)
@Configuration
@Slf4j
public class WebSecurityConfig implements WebMvcConfigurer {
    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;


    @Bean
    protected SecurityFilterChain configure(HttpSecurity http) throws Exception{
        http    .cors().and()
                .csrf().disable()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers("/","/auth/**").permitAll()
                        .shouldFilterAllDispatcherTypes(false)
                        .anyRequest()
                        .authenticated())
                .oauth2Login();

        return http.build();
    }


}

