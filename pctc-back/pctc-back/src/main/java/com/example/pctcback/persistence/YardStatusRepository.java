package com.example.pctcback.persistence;

import com.example.pctcback.model.YardStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
@Repository
public interface YardStatusRepository extends CrudRepository<YardStatus, Long > {
    @Query("SELECT COUNT (y.conNumber) FROM YardStatus y WHERE y.block = :block")
   Integer findConNumbersByBlock(@Param("block") String block);

}
