package com.example.pctcback.controller;

import com.example.pctcback.dto.ResponseDTO;
import com.example.pctcback.dto.UserDTO;
import com.example.pctcback.model.User;
import com.example.pctcback.security.TokenProvider;
import com.example.pctcback.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

@Slf4j
    @RestController
    @RequestMapping("/auth")
    public class UserController {
        @Autowired
        private UserService userService;
        @Autowired
        private TokenProvider tokenProvider;
        private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
        @PostMapping("/user/join")
        public ResponseEntity<?> SignupUser(@RequestBody UserDTO dto){
            try{
                if(dto == null || dto.getPassword() == null){
                    throw new RuntimeException("it's not valid.");
                }
                User Newuser = User.builder()
                                .username(dto.getUsername())
                                .password(passwordEncoder.encode(dto.getPassword()))
                                .nickname(dto.getNickname())
                        .build();
                Newuser = userService.create(Newuser);
                UserDTO registereduser = UserDTO.builder()
                        .id(Newuser.getId())
                        .nickname(Newuser.getNickname())
                        .username(Newuser.getUsername())
                        .build();

                return ResponseEntity.ok().body(registereduser);
            } catch (Exception e) {
                if ("Username already exists".equals(e.getMessage())) {
                    return ResponseEntity.status(HttpStatus.CONFLICT).body(e.getMessage());
                } else {
                    return ResponseEntity.badRequest().body(e.getMessage());
                }
            }}
        @PostMapping("/user/login")
        public ResponseEntity<?> authenticate (@RequestBody UserDTO dto){
            User user = userService.getByCredentials(
                    dto.getUsername(),
                    dto.getPassword(),
                    passwordEncoder
            );
            if(user !=null){
                final String token = tokenProvider.create(user);
//                HttpHeaders headers = new HttpHeaders();
//                headers.add(HttpHeaders.SET_COOKIE, ResponseCookie.from("token", token).build().toString());
                UserDTO responseUserDTO = UserDTO.builder()
                        .username(user.getUsername())
                        .id(user.getId())
                        .token(token)
                        .build();
                return ResponseEntity.ok().body(responseUserDTO);
            }else{
                ResponseDTO responseDTO = ResponseDTO.builder()
                        .error("Login failed.")
                        .build();
                return ResponseEntity.badRequest().body(responseDTO);
            }

        }

    }


