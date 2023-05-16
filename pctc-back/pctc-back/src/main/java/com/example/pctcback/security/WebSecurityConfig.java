package com.example.pctcback.security;

import lombok.extern.slf4j.Slf4j;
import org.apache.catalina.filters.CorsFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@EnableWebSecurity
@Configuration
@Slf4j
public class WebSecurityConfig implements WebMvcConfigurer {
    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;
    @Bean
    protected SecurityFilterChain configure(HttpSecurity http) throws Exception{
        http.cors()
                .and()
                .csrf().disable()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers("/","/auth/**").permitAll()
                        .shouldFilterAllDispatcherTypes(false)
                        .anyRequest()
                        .authenticated()
                );
        http.addFilterAfter(
                jwtAuthenticationFilter,
                CorsFilter.class
        );
        return http.build();
    }


}
