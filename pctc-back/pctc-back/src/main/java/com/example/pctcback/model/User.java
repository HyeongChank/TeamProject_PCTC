package com.example.pctcback.model;

import com.example.pctcback.AuthProvider;
import com.example.pctcback.Role;
import jakarta.persistence.*;
import lombok.*;


@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Table(name = "Users",uniqueConstraints = {@UniqueConstraint(columnNames = "username")})
public class User {

    @Id
    @GeneratedValue( strategy = GenerationType.UUID)
    private String id;
    @Column(nullable = false, length = 200)
    private String username;
    private String email;
    private String nickname;
    private String password;
    @Enumerated(EnumType.STRING)
    private AuthProvider authProvider; // kako, Naver,Google
    @Enumerated(EnumType.STRING)
    private Role role;
    private String refreshToken;

    public void authorizeUser(){
        this.role = Role.USER;
    }
}

