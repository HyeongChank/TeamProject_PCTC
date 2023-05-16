package com.example.pctcback.persistence;

import com.example.pctcback.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, String> {
    User findByname(String username);
    Boolean existsByUsername(String username);
    User findByUsernameAndPassword(String username, String password);

}
