<?php
/**
 * Statistics endpoint for the AI Server API.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api\Endpoints;

use SS_AI_Image_Search\Api\Client;
use SS_AI_Image_Search\Api\Response;
use SS_AI_Image_Search\Exceptions\Api\ApiException;

/**
 * Statistics endpoint class for statistics and metrics.
 */
class StatisticsEndpoint {

	/**
	 * API Client instance.
	 *
	 * @var Client
	 */
	private Client $client;

	/**
	 * Constructor.
	 *
	 * @param Client $client API Client instance.
	 */
	public function __construct( Client $client ) {
		$this->client = $client;
	}

	/**
	 * Get general statistics.
	 *
	 * @param array $params Additional parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_statistics( array $params = array() ): Response {
		$endpoint = 'statistics';

		return $this->client->get( $endpoint, $params );
	}

	/**
	 * Get search statistics.
	 *
	 * @param array $params Additional parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_search_statistics( array $params = array() ): Response {
		$endpoint = 'statistics/search';

		return $this->client->get( $endpoint, $params );
	}

	/**
	 * Get indexing statistics.
	 *
	 * @param array $params Additional parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_indexing_statistics( array $params = array() ): Response {
		$endpoint = 'statistics/indexing';

		return $this->client->get( $endpoint, $params );
	}

	/**
	 * Get performance statistics.
	 *
	 * @param array $params Additional parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_performance_statistics( array $params = array() ): Response {
		$endpoint = 'statistics/performance';

		return $this->client->get( $endpoint, $params );
	}

	/**
	 * Get usage statistics.
	 *
	 * @param array $params Additional parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_usage_statistics( array $params = array() ): Response {
		$endpoint = 'statistics/usage';

		return $this->client->get( $endpoint, $params );
	}

	/**
	 * Get error statistics.
	 *
	 * @param array $params Additional parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_error_statistics( array $params = array() ): Response {
		$endpoint = 'statistics/errors';

		return $this->client->get( $endpoint, $params );
	}

	/**
	 * Get statistics for a specific time period.
	 *
	 * @param string $period Time period (e.g., 'day', 'week', 'month').
	 * @param array  $params Additional parameters.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_period_statistics( string $period, array $params = array() ): Response {
		$endpoint = 'statistics/period';

		$query_params = array_merge(
			array(
				'period' => $period,
			),
			$params
		);

		return $this->client->get( $endpoint, $query_params );
	}

	/**
	 * Get top search queries.
	 *
	 * @param int $limit Maximum number of results.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_top_queries( int $limit = 10 ): Response {
		$endpoint = 'statistics/top-queries';

		$query_params = array(
			'limit' => $limit,
		);

		return $this->client->get( $endpoint, $query_params );
	}

	/**
	 * Get popular products.
	 *
	 * @param int $limit Maximum number of results.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_popular_products( int $limit = 10 ): Response {
		$endpoint = 'statistics/popular-products';

		$query_params = array(
			'limit' => $limit,
		);

		return $this->client->get( $endpoint, $query_params );
	}

	/**
	 * Get index statistics.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_index_statistics(): Response {
		$endpoint = 'statistics/index';

		return $this->client->get( $endpoint );
	}

	/**
	 * Get cache statistics.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_cache_statistics(): Response {
		$endpoint = 'statistics/cache';

		return $this->client->get( $endpoint );
	}
}