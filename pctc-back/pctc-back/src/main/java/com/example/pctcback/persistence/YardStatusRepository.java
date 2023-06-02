package com.example.pctcback.persistence;

import com.example.pctcback.model.YardStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.CrudRepository;

public interface YardStatusRepository extends CrudRepository<YardStatus, Long > {
}
