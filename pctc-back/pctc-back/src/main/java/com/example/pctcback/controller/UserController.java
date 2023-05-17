package com.example.pctcback.controller;

import com.example.pctcback.dto.UserDTO;
import com.example.pctcback.model.User;
import com.example.pctcback.security.TokenProvider;
import com.example.pctcback.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Slf4j
    @RestController
    @RequestMapping("/auth")
    public class UserController {
        @Autowired
        UserService userService;
        @GetMapping
        public ResponseEntity<?> getUsers(){
            return null;
        }

    }

