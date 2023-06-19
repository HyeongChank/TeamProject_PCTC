package com.example.pctcback.persistence;

import com.example.pctcback.model.BerthStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BerthStatusRepository extends JpaRepository<BerthStatus, Long> {
}
