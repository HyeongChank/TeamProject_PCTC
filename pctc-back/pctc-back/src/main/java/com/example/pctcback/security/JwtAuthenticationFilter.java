package com.example.pctcback.security;


import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.AuthorityUtils;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

    @Slf4j
    @Component
    public class JwtAuthenticationFilter extends OncePerRequestFilter {
        @Autowired
        private TokenProvider tokenProvider;

        @Override
        protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
            try {
                String token = parserBearerToken(request);
                log.info("Filter is running...");
                log.info("Token is.. " + token);
                if (token != null && !token.equalsIgnoreCase("null")) {
                    //토큰 검사
                    String userId = tokenProvider.validateAndGetUserId(token);
                    log.info("User ID: {}", userId); // 사용자 ID 로그 출력
                    AbstractAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(
                            userId,
                            null,
                            AuthorityUtils.NO_AUTHORITIES
                    );
                    authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                    SecurityContext securityContext = SecurityContextHolder.createEmptyContext();
                    securityContext.setAuthentication(authentication);
                    SecurityContextHolder.setContext(securityContext);
                }
            } catch (Exception e) {
                logger.error("Could not set user auth", e);
            }
            filterChain.doFilter(request, response);
        }
        private String parserBearerToken(HttpServletRequest request) {
            //HTTP 요청의 헤더 파싱- bearer 토큰 리턴
            String bearerToken = request.getHeader("Authorization");
            if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
                return bearerToken.substring(7);
            }
            return null;
        }
    }
