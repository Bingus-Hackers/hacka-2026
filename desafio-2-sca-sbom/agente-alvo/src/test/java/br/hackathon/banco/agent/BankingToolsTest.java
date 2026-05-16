package br.hackathon.banco.agent;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class BankingToolsTest {

    @Autowired BankingTools bankingTools;

    @Test
    void consultarSaldoDemo() {
        var result = bankingTools.consultarSaldo("DEMO-001");
        assertEquals("DEMO-001", result.get("conta_id"));
        assertTrue((Double) result.get("saldo_simulado") > 0);
    }

    @Test
    void explicarPix() {
        var result = bankingTools.explicarPix("limite");
        assertTrue(result.get("explicacao").toString().contains("Limite"));
    }
}
