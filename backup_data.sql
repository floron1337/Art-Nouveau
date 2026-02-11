--
-- PostgreSQL database dump
--

\restrict TG3ID8tD192CKBMckhHQn2HRrFljwVw2sXjpDC9AE5CmwbafwsLG3XSx4cDxMGb

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Art_Nouveau_award; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: Art_Nouveau_category; Type: TABLE DATA; Schema: public; Owner: floron
--

INSERT INTO public."Art_Nouveau_category" (category_id, name, description, icon_url, slug, icon_class) VALUES (3, 'Surrealism', 'Explored the subconscious mind and dreams, often featuring illogical scenes, strange creatures, and ordinary objects in impossible situations.', '', 'surrealism', 'fa fas fa-eye');
INSERT INTO public."Art_Nouveau_category" (category_id, name, description, icon_url, slug, icon_class) VALUES (2, 'Impressionism', 'Focused on capturing the fleeting effect of light and color in the immediate moment, often using loose brushwork and painting outdoors (en plein air).', '', 'impressionism', 'fa fas fa-palette');
INSERT INTO public."Art_Nouveau_category" (category_id, name, description, icon_url, slug, icon_class) VALUES (1, 'Renaissance', 'Characterized by realism, perspective, humanism, and a revival of classical Greek and Roman themes.', '', 'renaissance', 'fa fas fa-landmark');


--
-- Data for Name: Art_Nouveau_product; Type: TABLE DATA; Schema: public; Owner: floron
--

INSERT INTO public."Art_Nouveau_product" (id, name, description, author, price, stock, image, type, category_id) VALUES (1, 'Mona Lisa', '', 'Leonardo da Vinci', 34643, 0, '', '', 1);
INSERT INTO public."Art_Nouveau_product" (id, name, description, author, price, stock, image, type, category_id) VALUES (2, 'The Creation of Adam', '', 'Michelangelo', 5234, 0, '', '', 1);
INSERT INTO public."Art_Nouveau_product" (id, name, description, author, price, stock, image, type, category_id) VALUES (3, 'Impression, Sunrise', '', 'Claude Monet', 7654, 0, '', '', 2);
INSERT INTO public."Art_Nouveau_product" (id, name, description, author, price, stock, image, type, category_id) VALUES (4, 'Luncheon of the Boating Party', '', 'Pierre-Auguste Renoir', 7455, 0, '', '', 2);
INSERT INTO public."Art_Nouveau_product" (id, name, description, author, price, stock, image, type, category_id) VALUES (5, 'The Persistence of Memory', '', 'Salvador Dalí', 6534, 0, '', '', 3);
INSERT INTO public."Art_Nouveau_product" (id, name, description, author, price, stock, image, type, category_id) VALUES (7, 'Test', 'fdas gsdkfhg dsfkghd fskgdhfs gkdfsgjkdfhs gkdsfjhg kdsfjgh kdsfjhgkdsf gjdfhs gkjdfhksg jhsdkjgh kdfjsgh kdfs', 'Testulescu', 340.2, 5, '', 'Digital', 3);
INSERT INTO public."Art_Nouveau_product" (id, name, description, author, price, stock, image, type, category_id) VALUES (6, 'The Son of Man', '', 'René Magritte', 74579, 0, 'products/product_images/The-Son-of-Man.jpg', '', 3);


--
-- Data for Name: Art_Nouveau_award_products; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: Art_Nouveau_discount; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: Art_Nouveau_exhibition; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: Art_Nouveau_exhibition_products; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: Art_Nouveau_user; Type: TABLE DATA; Schema: public; Owner: floron
--

INSERT INTO public."Art_Nouveau_user" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone, country, county, city, address, code, email_confirmed) VALUES (9, 'pbkdf2_sha256$1200000$5Z7dIBsldqQBPTa4ohszcz$N1RtKJYLERL7LCBzAcQQD6cBYSqZNHkPszTFQTbG4bA=', NULL, false, 'test1', 'Florin', 'Venis', 'cioarama@gmail.com', false, true, '2026-01-03 19:58:08.273493+02', '0720985591', 'Romania', 'Constanta', '', '', '4d283e9f6f0e3a41f4682a748b407c0e', true);
INSERT INTO public."Art_Nouveau_user" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone, country, county, city, address, code, email_confirmed) VALUES (1, 'pbkdf2_sha256$1200000$dtX04Kwm7avfvAYMxKXEz2$P9me0pSmnjx/urE9wOCBC8WhxeE5LneppCYnDKqmaIM=', '2026-01-03 22:38:30.401973+02', true, 'floron', 'test', 'testulescu', 'abcd@gmail.com', true, true, '2026-01-03 15:46:07+02', '', '', '', '', '', NULL, true);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: Art_Nouveau_user_groups; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: floron
--

INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (5, 'Can add permission', 3, 'add_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (6, 'Can change permission', 3, 'change_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (7, 'Can delete permission', 3, 'delete_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (8, 'Can view permission', 3, 'view_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (9, 'Can add group', 2, 'add_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (10, 'Can change group', 2, 'change_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (11, 'Can delete group', 2, 'delete_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (12, 'Can view group', 2, 'view_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (21, 'Can add category', 7, 'add_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (22, 'Can change category', 7, 'change_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (23, 'Can delete category', 7, 'delete_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (24, 'Can view category', 7, 'view_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (25, 'Can add product', 10, 'add_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (26, 'Can change product', 10, 'change_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (27, 'Can delete product', 10, 'delete_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (28, 'Can view product', 10, 'view_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (29, 'Can add exhibition', 9, 'add_exhibition');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (30, 'Can change exhibition', 9, 'change_exhibition');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (31, 'Can delete exhibition', 9, 'delete_exhibition');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (32, 'Can view exhibition', 9, 'view_exhibition');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (33, 'Can add discount', 8, 'add_discount');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (34, 'Can change discount', 8, 'change_discount');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (35, 'Can delete discount', 8, 'delete_discount');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (36, 'Can view discount', 8, 'view_discount');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (37, 'Can add award', 6, 'add_award');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (38, 'Can change award', 6, 'change_award');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (39, 'Can delete award', 6, 'delete_award');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (40, 'Can view award', 6, 'view_award');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (41, 'Can add user', 11, 'add_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (42, 'Can change user', 11, 'change_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (43, 'Can delete user', 11, 'delete_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (44, 'Can view user', 11, 'view_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (45, 'Can add user product view', 12, 'add_userproductview');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (46, 'Can change user product view', 12, 'change_userproductview');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (47, 'Can delete user product view', 12, 'delete_userproductview');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (48, 'Can view user product view', 12, 'view_userproductview');


--
-- Data for Name: Art_Nouveau_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: Art_Nouveau_userproductview; Type: TABLE DATA; Schema: public; Owner: floron
--

INSERT INTO public."Art_Nouveau_userproductview" (id, view_date, product_id, user_id) VALUES (5, '2026-01-03 22:40:51.428038+02', 4, 1);
INSERT INTO public."Art_Nouveau_userproductview" (id, view_date, product_id, user_id) VALUES (7, '2026-01-03 22:49:28.978149+02', 3, 1);
INSERT INTO public."Art_Nouveau_userproductview" (id, view_date, product_id, user_id) VALUES (22, '2026-01-03 23:10:56.630577+02', 6, 1);
INSERT INTO public."Art_Nouveau_userproductview" (id, view_date, product_id, user_id) VALUES (27, '2026-01-03 23:11:40.9904+02', 7, 1);
INSERT INTO public."Art_Nouveau_userproductview" (id, view_date, product_id, user_id) VALUES (28, '2026-01-03 23:12:16.163138+02', 1, 1);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: floron
--



--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: floron
--

INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (1, '2026-01-03 16:36:24.786411+02', '1', 'floron', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (2, '2026-01-03 19:35:39.283233+02', '2', 'fdsa', 3, '', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (3, '2026-01-03 19:35:39.283256+02', '3', 'geasg', 3, '', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (4, '2026-01-03 19:35:39.283266+02', '4', 'hgdfhdf', 3, '', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (5, '2026-01-03 19:45:21.830803+02', '5', 'fdsag', 3, '', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (6, '2026-01-03 19:51:12.7005+02', '6', 'test1', 3, '', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (7, '2026-01-03 19:54:57.472807+02', '7', 'test1', 3, '', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (8, '2026-01-03 19:57:55.507244+02', '8', 'test1', 3, '', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (9, '2026-01-03 20:27:26.923135+02', '9', 'test1', 2, '[{"changed": {"fields": ["password"]}}]', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (10, '2025-12-23 19:05:57.280154+02', '3', 'Surrealism', 2, '[{"changed": {"fields": ["Icon class"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (11, '2025-12-23 19:06:10.3595+02', '2', 'Impressionism', 2, '[{"changed": {"fields": ["Icon class"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (12, '2025-12-23 19:06:15.713649+02', '1', 'Renaissance', 2, '[{"changed": {"fields": ["Icon class"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (13, '2026-01-03 22:38:26.499186+02', '1', 'floron', 2, '[{"changed": {"fields": ["Email confirmed"]}}]', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (14, '2026-01-03 22:50:26.48472+02', '6', 'The Son of Man', 2, '[{"changed": {"fields": ["Image"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (15, '2026-01-03 22:53:14.331766+02', '6', 'The Son of Man', 2, '[{"changed": {"fields": ["Image"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (16, '2026-01-03 22:53:28.347051+02', '6', 'The Son of Man', 2, '[{"changed": {"fields": ["Image"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (17, '2026-01-03 23:00:45.999071+02', '6', 'The Son of Man', 2, '[{"changed": {"fields": ["Price"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (18, '2026-01-03 23:01:06.676583+02', '6', 'The Son of Man', 2, '[{"changed": {"fields": ["Image"]}}]', 10, 1);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: floron
--

INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('vmp2jbzk11qzd1av2956menkl4psxan0', '.eJxVjDEOgzAQBP_iOrJsc_hwyvS8AZm7IyaJbAlDFeXvAYkiabbYmd23GuK2pmGrsgwzq6uy6vLbjZGekg_Aj5jvRVPJ6zKP-lD0SavuC8vrdrp_BynWtK-p7RAQJXSBwZqmnUJ04o1DmphCg2CdD8TSQgASiOysxz09GmYL6vMFyQk3WQ:1vY20I:Yd1mvja8LiU5JG4ySgKBZ2kzr5yDCxcwFp34wk2nXNo', '2026-01-06 15:00:42.820232+02');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('2lmm1k9rcoul527oikd1v9qiqwwxb53z', '.eJxVjEEOwiAURO_C2pBPS6F06d4zED58LGqgKW2iMd7dNulClzPz5r2Zdesy2rXSbFNgAxPs9Nuh83fK-xBuLl8L9yUvc0K-I_xYK7-UQI_zwf4JRlfH7a1C6JTvMTpAMr2O0aGQPoKgoDqldSe8AGmkiC0aA9C0uEUMELHVjdmllWpNJVt6Tml-saFXEuDzBZ7XP94:1vc8OM:--h2vSmIn_0fIRqkp1Z_7mcW_7anJvVkNwasDRhPCsM', '2026-01-04 22:38:30.406738+02');


--
-- Name: Art_Nouveau_award_award_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_award_award_id_seq"', 1, false);


--
-- Name: Art_Nouveau_award_products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_award_products_id_seq"', 1, false);


--
-- Name: Art_Nouveau_category_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_category_category_id_seq"', 3, true);


--
-- Name: Art_Nouveau_discount_discount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_discount_discount_id_seq"', 1, false);


--
-- Name: Art_Nouveau_exhibition_exhibition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_exhibition_exhibition_id_seq"', 1, false);


--
-- Name: Art_Nouveau_exhibition_products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_exhibition_products_id_seq"', 1, false);


--
-- Name: Art_Nouveau_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_product_id_seq"', 7, true);


--
-- Name: Art_Nouveau_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_user_groups_id_seq"', 1, false);


--
-- Name: Art_Nouveau_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_user_id_seq"', 9, true);


--
-- Name: Art_Nouveau_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_user_user_permissions_id_seq"', 1, false);


--
-- Name: Art_Nouveau_userproductview_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public."Art_Nouveau_userproductview_id_seq"', 28, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 48, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 18, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 12, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: floron
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 21, true);


--
-- PostgreSQL database dump complete
--

\unrestrict TG3ID8tD192CKBMckhHQn2HRrFljwVw2sXjpDC9AE5CmwbafwsLG3XSx4cDxMGb

