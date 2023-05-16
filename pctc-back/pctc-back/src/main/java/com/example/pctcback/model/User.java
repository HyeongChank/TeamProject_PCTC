package com.example.pctcback.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.management.relation.Role;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "Users",uniqueConstraints = {@UniqueConstraint(columnNames = "username")})
public class User {

    @Id
    @GeneratedValue( strategy = GenerationType.IDENTITY)
    private String id;
    @Column(nullable = false)
    private String username;
    private String nickname;
    private String password;
    private Role role;
    private String authProvider;

}
