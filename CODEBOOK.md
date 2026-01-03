# Preliminary Codebook: California Food Retail Classification

**Project:** Classifying Food Retail Environments in California  
**Version:** 1.0 (Preliminary)  
**Last Updated:** December 2024  

---

## Overview

This codebook defines the coding rules for manually classifying food retail locations in California using a **Multi-Label Classification** system. Each location is coded independently on two orthogonal axes:

| Axis | Variable | Type | Purpose |
|------|----------|------|---------|
| Format | `MANUAL_FORMAT` | Categorical | Physical retail environment and service model |
| Ethnicity | `IS_ETHNIC` | Binary (0/1) | Cultural orientation of product assortment |

**Data Source:** Overture Maps Places dataset, filtered for grocery/food retail categories  
**Verification Method:** Google Street View imagery and satellite view ("Virtual Ground Truthing")

---

## Variable 1: MANUAL_FORMAT

### Definition

`MANUAL_FORMAT` captures the **physical retail format** and **service model** of the store, independent of its cultural orientation. This variable answers: *"What kind of shopping experience does this store provide?"*

### Valid Values

| Value | Label |
|-------|-------|
| `Supermarket` | Full-service grocery retail |
| `Convenience` | Limited-service, grab-and-go retail |
| `Other` | Non-standard or non-retail |

---

### Value: `Supermarket`

**Definition:** A full-service grocery store designed for comprehensive household provisioning, where customers self-select products and complete purchases at dedicated checkout stations.

**Required Criteria (ALL must be observable or reasonably inferred):**

1. **Self-Service Format**
   - Shopping carts and/or hand baskets available
   - Customers navigate aisles independently

2. **Fresh Department Presence**
   - At minimum: 2+ aisles OR dedicated sections of fresh produce
   - AND: Visible meat/seafood section (counter or packaged)

3. **General Merchandise**
   - At minimum: 2+ aisles of non-food household goods (cleaning supplies, paper products, etc.)

4. **Checkout Infrastructure**
   - Multiple checkout lanes OR dedicated cashier stations
   - NOT: Single counter service only

**Indicative Features (supportive but not required):**
- Parking lot visible
- Shopping cart corrals
- Storefront wider than ~50 feet
- Visible department signage (Produce, Dairy, Meat, etc.)

**Chain Examples:** Safeway, Ralphs, Whole Foods, Trader Joe's, WinCo, Food 4 Less, Sprouts

---

### Value: `Convenience`

**Definition:** A limited-service retail outlet focused on immediate consumption, quick transactions, and a narrow product assortment. These stores prioritize speed and accessibility over comprehensive selection.

**Required Criteria (ANY of the following):**

1. **Limited Physical Footprint**
   - Single-aisle or open-floor layout
   - No shopping carts (hand baskets only or none)

2. **Counter-Dominant Service**
   - Primary transaction point is a single counter
   - Often includes tobacco/lottery/alcohol behind counter

3. **Product Mix Indicators**
   - High proportion of processed/packaged foods
   - Limited or no fresh produce (may have bananas, single cooler of fruit)
   - Beverage coolers as primary refrigeration

4. **Contextual Indicators**
   - Attached to gas station
   - Storefront signage emphasizes non-grocery services (ATM, lottery, check cashing)

**Subcategories (all coded as `Convenience`):**
- Gas station markets (Chevron ExtraMile, Shell, ARCO ampm)
- Traditional convenience stores (7-Eleven, Circle K)
- Corner stores / Bodegas
- Liquor stores with grocery items
- Mini-marts

**Chain Examples:** 7-Eleven, ampm, Circle K, Wawa, QuikStop

---

### Value: `Other`

**Definition:** Locations that do not fit the Supermarket or Convenience classification, including non-retail food distribution, specialty-only retail, or data errors.

**Assign `Other` when:**

| Situation | Example |
|-----------|---------|
| Farmers market or outdoor market | Weekly produce market in parking lot |
| Wholesale/distribution only | Restaurant supply warehouse |
| Specialty single-category | Butcher shop, bakery, cheese shop (no grocery) |
| Non-food retail misclassified | Dollar store, pharmacy, pet store |
| Permanently closed | Visible "Closed" signage, empty storefront |
| Cannot be verified | No Street View coverage, ambiguous imagery |

**Note:** If a specialty store (e.g., butcher) also sells grocery items and functions as a neighborhood provisioning point, consider coding as `Convenience` rather than `Other`.

---

## Variable 2: IS_ETHNIC

### Definition

`IS_ETHNIC` captures whether the store's **primary identity, branding, and product assortment** is oriented toward serving a **specific cultural or ethnic community**, as opposed to the general population.

This variable answers: *"Would a customer unfamiliar with this culture face meaningful barriers (language, product knowledge, cultural context) to shopping here comfortably?"*

### Valid Values

| Value | Label | Meaning |
|-------|-------|---------|
| `1` | Ethnic | Specific dominant cultural focus |
| `0` | General | Broad audience, no dominant cultural orientation |

---

### Value: `1` (Ethnic)

**Definition:** The store's signage, branding, product assortment, and/or customer base is **predominantly oriented toward a specific cultural or ethnic community**.

**Coding Triggers (ANY of the following):**

1. **Signage & Branding**
   - Primary storefront signage in non-English language
   - Store name explicitly references culture/nationality (e.g., "Mercado," "Asian Mart," "Halal Market")
   - Cultural imagery or flags prominently displayed

2. **Product Specialization**
   - Majority of visible products serve a specific cuisine/culture
   - Specialty imports not available in general supermarkets
   - Cultural-specific departments (e.g., live seafood tanks, tortilleria, halal butcher)

3. **Known Ethnic Chains**
   - 99 Ranch Market (Asian)
   - H Mart (Korean/Asian)
   - Vallarta Supermarkets (Hispanic)
   - Northgate Market (Hispanic)
   - Super King (Middle Eastern/Armenian)
   - Zion Market (Korean)
   - Marukai (Japanese)

**Cultural Categories (non-exhaustive):**
- Hispanic/Latino (Mercado, Carniceria, Supermercado)
- East Asian (Chinese, Korean, Japanese, Vietnamese markets)
- South Asian (Indian, Pakistani grocery)
- Middle Eastern (Halal, Persian, Armenian markets)
- Eastern European (Russian, Polish delis)
- African (Ethiopian, Nigerian markets)
- Filipino (Filipino grocery, Seafood City)

---

### Value: `0` (General)

**Definition:** The store targets the **general population** without a dominant cultural orientation, OR offers broad multicultural variety without specific cultural focus.

**Coding Triggers:**

1. **Mainstream Chains**
   - Major national/regional chains (Safeway, Kroger, Walmart, Target)
   - Natural/organic chains (Whole Foods, Sprouts, Trader Joe's)

2. **Generic Independent Stores**
   - Name does not reference specific culture
   - English-dominant signage
   - Standard American grocery assortment

3. **"International" Variety Stores (IMPORTANT EDGE CASE)**

> **Special Rule:** Stores named "International Market," "World Market," "Global Foods," or similar that sell diverse products from **multiple regions without a dominant cultural focus** should be coded as `IS_ETHNIC = 0`.

**Rationale:** These stores function as variety/specialty stores with low cultural barriers to entry. They cater to adventurous general consumers seeking diverse products, rather than serving as provisioning points for specific cultural communities.

**Examples to code as `0`:**
- Cost Plus World Market
- "International Grocery" with visible products from 5+ distinct regions
- "World Foods" with no dominant language on signage

**Contrast with `1`:** A store named "International Market" but where Street View shows predominantly Asian products, Korean signage, and Korean-language newspapers → Code as `1`.

---

### Edge Cases and Decision Rules

| Scenario | IS_ETHNIC | Rationale |
|----------|-----------|-----------|
| Trader Joe's (diverse international products) | 0 | Targets general "foodie" audience, American branding |
| Whole Foods (large Asian food section) | 0 | Section within general store, mainstream branding |
| "La Michoacana" meat market | 1 | Hispanic cultural focus despite small size |
| Indian spice shop (specialty only) | 1* | Ethnic focus, but consider `Other` for MANUAL_FORMAT if not grocery |
| Store with bilingual signage (English + Spanish) | Context-dependent | If Hispanic products dominate → 1; If general stock with Spanish for accessibility → 0 |
| Costco (diverse membership base) | 0 | Mainstream wholesale, general audience |

---

## Coding Examples

The following examples illustrate how to apply both variables together:

| Store Name | MANUAL_FORMAT | IS_ETHNIC | Rationale |
|------------|---------------|-----------|-----------|
| **7-Eleven** | Convenience | 0 | Limited selection, counter service, mainstream chain |
| **Safeway** | Supermarket | 0 | Full-service, mainstream American chain |
| **Vallarta Supermarkets** | Supermarket | 1 | Full-service format (carts, produce aisles, checkout lanes) with dominant Hispanic focus (Spanish signage, tortilleria, carniceria) |
| **Cost Plus World Market** | Other | 0 | Specialty/gift retail, not primary grocery; broad international variety without cultural focus |
| **99 Ranch Market** | Supermarket | 1 | Full-service Asian supermarket with Chinese/pan-Asian focus |
| **Corner Liquor & Grocery** | Convenience | 0 | Limited selection, counter service, general convenience items |
| **Carniceria El Pueblo** | Convenience | 1 | Small format, limited scope, but clear Hispanic cultural focus |
| **H Mart** | Supermarket | 1 | Large format Korean/Asian chain with full departments |
| **Grocery Outlet** | Supermarket | 0 | Full-service discount format, general audience |
| **Mercado La Paloma** | Convenience | 1 | Small neighborhood market, Hispanic focus |

---

## Coding Procedure

### Step 1: Locate the Store
1. Open Google Maps using the provided coordinates or Street View URL
2. Identify the storefront in Street View
3. If Street View unavailable, use satellite imagery and nearby context

### Step 2: Assess MANUAL_FORMAT
Ask in order:
1. Can I see shopping carts or multiple checkout lanes? → Likely `Supermarket`
2. Is it attached to a gas station or is the storefront very small? → Likely `Convenience`
3. Is it a farmers market, warehouse, or non-grocery retail? → `Other`
4. If uncertain, default to `Convenience` for small independents

### Step 3: Assess IS_ETHNIC
Ask in order:
1. Is the primary signage in a non-English language? → Likely `1`
2. Does the store name reference a specific culture? → Likely `1`
3. Is it a known ethnic chain (see list above)? → `1`
4. Is it "International/World" with no dominant culture visible? → `0`
5. Is it a mainstream chain or generic independent? → `0`
6. If uncertain, default to `0`

### Step 4: Record and Note
- Enter values in `MANUAL_FORMAT` and `IS_ETHNIC` columns
- If the decision was difficult, add a brief note in a separate `NOTES` column (optional)

---

## Quality Control

### Inter-Rater Reliability
If multiple coders are involved:
- Code a shared subset of 20 locations independently
- Calculate Cohen's Kappa for each variable
- Discuss and resolve discrepancies before proceeding

### Confidence Flags (Optional)
Consider adding a `CONFIDENCE` column:
- `H` (High): Clear-cut case, high-quality Street View
- `M` (Medium): Some ambiguity, but reasonable judgment
- `L` (Low): Poor imagery, uncertain classification

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | December 2024 | Initial preliminary codebook |

---

## Contact

For questions about coding decisions or edge cases, document the case with a screenshot and coordinates for team discussion.
