package com.example.pctcback.security;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.example.pctcback.model.User;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Date;

@Slf4j
@Service
public class TokenProvider {
    @Value("${my.secretary}")
    private String SECRET_KEY;

    public String create(User userEntity) {
        // 기한 - 1일
        Date expiryDate = Date.from(
                Instant.now()
                        .plus(1, ChronoUnit.DAYS));
        Algorithm algorithm = Algorithm.HMAC512(SECRET_KEY);
        // JWT Token 생성
        return JWT.create()
                .withSubject(userEntity.getUsername())
                .withIssuer("PCTC project")
                .withIssuedAt(expiryDate)
                .sign(algorithm);
    }
    public String validateAndGetUserId(String token){
        //parseClaimJWws method 가 base64로 디코딩- 파싱이 이루어진다.
        // 헤더- 페이로드를 setSigningkey 로 넘어온 시크릿을 이용해서명 -token 과 비교
        // 위조 되지 안항ㅆ으면 페이로드 리턴, 위조면 예외
        // 여기서 getBody 로 Body에 있는 Userid 를 가져온다.
        Algorithm algorithm = Algorithm.HMAC512(SECRET_KEY);
        log.debug("TokenProvider: token: {}", token);
        DecodedJWT jwt = JWT.require(algorithm)
                .build()
                .verify(token);
        return jwt.getSubject();

    }
}
