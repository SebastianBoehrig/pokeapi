from unittest.mock import AsyncMock, call, patch

import httpx
import pytest

from app.logic import get_types


@pytest.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client


@patch('app.logic.get_types.get_type', new_callable=AsyncMock)
@patch('app.logic.get_types.get_all_types', new_callable=AsyncMock)
async def test_get_types(get_all_types_mock, get_type_mock, async_client):
    get_all_types_mock.return_value = {
        'results': [
            {'name': 't1'},
            {'name': 't2'},
            {'name': 't3'},
        ]
    }
    get_type_mock.side_effect = [
        {'name': 't1_name', 'sprites': {'generation-ix': {'scarlet-violet': {'name_icon': 't1_image_url'}}}},
        {'name': 't2_name', 'sprites': {'generation-ix': {'scarlet-violet': {'name_icon': 't2_image_url'}}}},
        {'name': 't3_name', 'sprites': {'generation-ix': {'scarlet-violet': {'name_icon': 't3_image_url'}}}},
    ]

    assert await get_types.get_types(async_client) == [
        {'name': 't1_name', 'img': 't1_image_url'},
        {'name': 't2_name', 'img': 't2_image_url'},
        {'name': 't3_name', 'img': 't3_image_url'},
    ]
    calls = [call('t1', async_client), call('t2', async_client), call('t3', async_client)]
    get_type_mock.assert_has_awaits(calls)


@pytest.mark.parametrize(
    'sprites, img',
    [
        ({'generation-iv': {'platinum': {'name_icon': 't1_image_url'}}}, 't1_image_url'),
        (
            {
                'generation-ix': {'scarlet-violet': {'name_icon': None}},
                'generation-iv': {'platinum': {'name_icon': 't1_image_url'}},
            },
            't1_image_url',
        ),
        ({'generation-ix': {'scarlet-violet': {'name_icon': None}}}, None),
        ({}, None),
    ],
)
@patch('app.logic.get_types.get_type', new_callable=AsyncMock)
@patch('app.logic.get_types.get_all_types', new_callable=AsyncMock)
async def test_get_types_backup_sprites(get_all_types_mock, get_type_mock, async_client, sprites, img):
    get_all_types_mock.return_value = {'results': [{'name': 't1'}]}
    get_type_mock.return_value = {'name': 't1_name', 'sprites': sprites}

    expected = [{'name': 't1_name', 'img': img}] if img else []
    assert await get_types.get_types(async_client) == expected


@patch('app.logic.get_types.get_all_types', new_callable=AsyncMock)
async def test_get_types_no_types(get_all_types_mock, async_client):
    get_all_types_mock.return_value = {'results': []}

    assert await get_types.get_types(async_client) == []
