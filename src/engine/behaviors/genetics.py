import random

def apply_mutation(parent_attrs):
    """
    Copia los atributos del padre y les aplica una variación 
    basada en el mutation_rate.
    """
    child_attrs = parent_attrs.copy()
    m_rate = child_attrs.get("mutation_rate", 0.1)
    
    for key in ["metabolic_rate", "reproduction_threshold", "intelligence", "speed", "resilience"]:
        if key in child_attrs:
            # Variación entre -mutation_rate y +mutation_rate
            variation = 1 + random.uniform(-m_rate, m_rate)
            child_attrs[key] *= variation
    
    # Hard limits para evitar valores imposibles (ej. metabolismo negativo)
    child_attrs["metabolic_rate"] = max(0.5, child_attrs["metabolic_rate"])
    child_attrs["intelligence"] = max(0.01, child_attrs["intelligence"])
    
    return child_attrs